import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from bot2.buttons import create_keyboard_markup
from bot2.api import create_user, set_user_language, get_user_language
import requests
import bleach
from bot2.api import BASE_URL
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import OrderState, CartState


API_TOKEN = '6051249815:AAH14Wsz2CopO-Q7o-Yu0gWsYW3bXhwMB5s'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, proxy='http://proxy.server:3128')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user = message.from_user
    if create_user(user.username, user.first_name, user.id):
        await message.reply("Assalomu alekum\nPowermax botiga xush kelibsiz.", reply_markup=create_keyboard_markup(get_user_language(user.id)))
    else:
        await message.reply("You are not logged in. Please log in to continue.")

@dp.message_handler(lambda message: message.text in ["🇺🇿 Tilni o'zgartirish", "🇷🇺 Изменить язык"])
async def select_language(message: types.Message):
    language_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    language_markup.add(KeyboardButton(text="🇺🇿 O'zbek"), KeyboardButton(text="🇷🇺 Русский"))
    await message.reply("Tilni tanlang:" if get_user_language(message.from_user.id)=="uz" else "Выберите язык", reply_markup=language_markup)


@dp.message_handler(lambda message: message.text in ["🇺🇿 O'zbek", "🇷🇺 Русский"])
async def handle_language_selection(message: types.Message):
    user = message.from_user
    if message.text == "🇺🇿 O'zbek":
        set_user_language(user.id, "uz")
        await message.reply("Til muvaffaqiyatli o'zgartirildi: O'zbek", reply_markup=create_keyboard_markup(get_user_language(user.id)))
    elif message.text == "🇷🇺 Русский":
        set_user_language(user.id, "ru")
        await message.reply("Язык успешно изменен: Русский", reply_markup=create_keyboard_markup(get_user_language(user.id)))


@dp.message_handler(lambda message: message.text in ["❓ Yordam", "❓ Помощь"])
async def send_welcome(message: types.Message):
    user = message.from_user
    text = "🛠 Mahsulotlar bo'limida siz Powermax dokonlaridagi mahsulotlarini ko'rish imkoniyatiga ega bo'lasiz\n🛒 Savat bo'limida siz olmoqchi bo'lgan mahsulotlaringizni saqlash imkoniga ega bo'lasiz\n🚚 Buyurtmalar bo'limida sizga yetkazib beriladigan mahsulotlarni ko'rishingiz mumkin\n🇺🇿 Tilni o'zgartirish bo'limida siz botning tilini o'zgartirish imkoniyatiga ega bo'lasiz\n☎️ Bog'lanish bo'limida biz bilan bog'lanishingiz mumkin bo'lgan Powermax kontaktlarini ko'rishingiz mumkin." if get_user_language(user.id)=='uz' else "В разделе 🛠 Продукты вы сможете увидеть продукты в магазинах Powermax\nВ разделе 🛒 Корзина вы сможете сохранить товары, которые хотите купить\nВ разделе 🚚 Заказы вы сможете доставить вам, вы можете увидеть продукты\nВ разделе 🇷🇺 Изменить язык у вас будет возможность изменить язык бота\nВ разделе ☎️ Контакты вы можете увидеть контакты Powermax, с которыми вы можете связаться с нами."
    await message.reply(text, reply_markup=create_keyboard_markup(get_user_language(user.id)))


@dp.message_handler(lambda message: message.text in ["☎️ Bog'lanish", "☎️ Связь"])
async def send_welcome(message: types.Message):
    user = message.from_user
    text = "Bog'lanish uchun\n☎️+998997663681\nga murojat qiling." if get_user_language(user.id)=='uz' else "Свяжитесь с нами по телефону\n☎️+998997663681."
    await message.reply(text, reply_markup=create_keyboard_markup(get_user_language(user.id)))


async def show_products(message: types.Message, products, data, lan):
    for product in products:
        if lan=='uz':
            product_details = f"<b>✅ Brendi:</b> {product['brend']}\n" \
                              f"<b>✅ Nomi:</b> {product['name_uz']}\n" \
                              f"<b>✅ Narxi:</b> ${product['sotish_narx']}\n"
        else:
            product_details = f"<b>✅ Бренд:</b> {product['brend']}\n" \
                              f"<b>✅ Наименование:</b> {product['name_ru']}\n" \
                              f"<b>✅ Цена:</b> ${product['sotish_narx']}\n"
        if product['xarakteristika_uz']:
            if lan=='uz': product_details += f"<b>✅ Xarakteristikasi:</b>\n{bleach.clean(product['xarakteristika_uz'], tags=[], attributes={}, strip=True)}"
            else: product_details += f"<b>✅ Характеристика:</b>\n{bleach.clean(product['xarakteristika_ru'], tags=[], attributes={}, strip=True)}"
        add_keyboard = InlineKeyboardMarkup(row_width=2)
        buyurtma_button = InlineKeyboardButton('🚚 Buyurtma berish' if lan=='uz' else "🚚 Разместить заказ", callback_data='add_buyurtma='+str(product['id']))
        add_keyboard.insert(buyurtma_button)
        savat_button = InlineKeyboardButton("🛒 Savatga qo'shish" if lan=='uz' else "🛒 В корзину", callback_data='add_savat='+str(product['id']))
        add_keyboard.insert(savat_button)
        if product['image']:
            await bot.send_photo(message.chat.id, photo=product['image'], caption=product_details, parse_mode='HTML', reply_markup=add_keyboard)
        else:
            await message.answer(product_details, parse_mode="HTML", reply_markup=add_keyboard)
    
    previous_page = data.get("previous")
    next_page = data.get("next")
    keyboard = InlineKeyboardMarkup(row_width=2)
    if previous_page:
        try: id = previous_page[5+previous_page.index('?page'):]
        except: id = '=1'
        prev_button = InlineKeyboardButton("⬅️ " + ("Oldingi" if lan=='uz' else "Предыдущий"), callback_data="prev_page"+id)
        keyboard.insert(prev_button)
    if next_page:
        id = next_page[5+next_page.index('?page'):]
        next_button = InlineKeyboardButton(("Keyingi" if lan=='uz' else "Следущая") + " ➡️", callback_data="next_page"+id)
        keyboard.insert(next_button)
    
    # Send pagination buttons
    await message.answer("Boshqa maxsulotlarni ko'rish:" if lan=='uz' else "Посмотреть другие товары:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["🛠 Mahsulotlar", "🛠 Продукты"])
async def handle_show_products(message: types.Message):
    response = requests.get(BASE_URL + "/products/")
    if response.status_code == 200:
        data = response.json()
        products = data.get("results", [])
        lan = get_user_language(message.from_user.id)
        await show_products(message, products, data, lan)


@dp.callback_query_handler(lambda query: query.data.startswith("prev_page"))
async def handle_previous_page(callback_query: types.CallbackQuery):
    previous_page_url = BASE_URL + '/products/?page'+ callback_query.data[9:]
    
    if previous_page_url:
        response = requests.get(previous_page_url)
        if response.status_code == 200:
            data = response.json()
            products = data.get("results", [])
            lan = get_user_language(callback_query.from_user.id)
            await show_products(callback_query.message, products, data, lan)


@dp.callback_query_handler(lambda query: query.data.startswith("next_page"))
async def handle_next_page(callback_query: types.CallbackQuery):
    next_page_url = BASE_URL + '/products/?page'+ callback_query.data[9:]

    if next_page_url:
        response = requests.get(next_page_url)
        if response.status_code == 200:
            data = response.json()
            products = data.get("results", [])
            lan = get_user_language(callback_query.from_user.id)
            await show_products(callback_query.message, products, data, lan)

@dp.callback_query_handler(lambda query: query.data.startswith("add_buyurtma="))
async def handle_add_buyurtma_page(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    lan = get_user_language(user_id)
    product_id = callback_query.data.replace("add_buyurtma=", "")
    await state.update_data(product_id=product_id)
    await bot.send_message(callback_query.from_user.id, "🔰 Nechta buyurtma bermoqchisiz?" if lan=='uz' else "🔰 Сколько вы хотите заказать?")
    
    # Set the quantity state
    await OrderState.quantity.set()

@dp.message_handler(state=OrderState.quantity)
async def handle_quantity(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lan = get_user_language(user_id)
    quantity = int(message.text)
    await state.update_data(quantity=quantity)
    
    # Ask the user for the location
    await message.answer("📍 Manzilni kiriting:" if lan=='uz' else "📍 Введите адрес:")
    
    # Set the location state
    await OrderState.location.set()

@dp.message_handler(state=OrderState.location)
async def handle_location(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lan = get_user_language(user_id)
    location = message.text
    await state.update_data(location=location)
    
    # Ask the user for the phone number
    await message.answer("📞 Telefon raqamingizni kiriting:" if lan=='uz' else "📞 Введите свой номер телефона:")
    
    # Set the phone_number state
    await OrderState.phone_number.set()

@dp.message_handler(state=OrderState.phone_number)
async def handle_phone_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lan = get_user_language(user_id)
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    
    # Get the accumulated data
    data = await state.get_data()
    
    # Make API request to add the order
    api_url = BASE_URL+"/buyurtma/"
    payload = {
        "product": data['product_id'],
        "count": data['quantity'],
        "location": data['location'],
        "tel": data['phone_number'],
        "user": user_id
    }
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 201:
        # Order successfully added
        await message.answer("✅ Buyurtmangiz muvaffaqiyatli amalga oshirildi. Siz bilan tez orada aloqaga chiqamiz." if lan=='uz' else "✅ Ваш заказ успешно выполнен. Мы свяжемся с вами в ближайшее время.")
    else:
        # Error occurred while adding the order
        await message.answer("⚠️ Xatolik yuz berdi" if lan == 'uz' else "⚠️ Произошла ошибка")
    
    # Reset the state
    await state.finish()


@dp.callback_query_handler(lambda query: query.data.startswith("add_savat="))
async def handle_add_savat_page(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    lan = get_user_language(user_id)
    product_id = callback_query.data.replace("add_savat=", "")
    await state.update_data(product_id=product_id)
    await bot.send_message(callback_query.from_user.id, "🔰 Nechta buyurtma bermoqchisiz?" if lan=='uz' else "🔰 Сколько вы хотите заказать?")
    
    await CartState.quantity.set()

@dp.message_handler(state=CartState.quantity)
async def handle_quantity(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lan = get_user_language(user_id)
    quantity = int(message.text)
    await state.update_data(quantity=quantity)
    
    # Ask the user for the location
    await message.answer("📍 Manzilni kiriting:" if lan=='uz' else "📍 Введите адрес:")
    
    # Set the location state
    await CartState.location.set()

@dp.message_handler(state=CartState.location)
async def handle_location(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lan = get_user_language(user_id)
    location = message.text
    await state.update_data(location=location)
    
    # Ask the user for the phone number
    await message.answer("📞 Telefon raqamingizni kiriting:" if lan=='uz' else "📞 Введите свой номер телефона:")
    
    # Set the phone_number state
    await CartState.phone_number.set()

@dp.message_handler(state=CartState.phone_number)
async def handle_phone_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lan = get_user_language(user_id)
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    
    # Get the accumulated data
    data = await state.get_data()
    
    # Make API request to add the order
    api_url = BASE_URL+"/savat/"
    payload = {
        "product": data['product_id'],
        "count": data['quantity'],
        "location": data['location'],
        "tel": data['phone_number'],
        "user": user_id
    }
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 201:
        await message.answer("✅ Buyurtmangiz muvaffaqiyatli savatga tushirildi" if lan=='uz' else "✅ Ваш заказ успешно добавлен в корзину")
    else:
        await message.answer("⚠️ Xatolik yuz berdi" if lan == 'uz' else "⚠️ Произошла ошибка")
    await state.finish()

# Buyurtmalar
@dp.message_handler(lambda message: message.text in ["🚚 Buyurtmalar", "🚚 Заказы"])
async def handle_buyurtmalar(message: types.Message):
    user_id = message.from_user.id
    lan = get_user_language(user_id)
    
    # Make a request to retrieve the user's orders
    api_url = BASE_URL + f'/buyurtma-list/{user_id}/'
    response = requests.get(api_url)
    orders = response.json()
    
    if response.status_code == 200:
        if not orders:
            await message.answer("📭 Sizda hech qanday buyurtma yo'q" if lan=='uz' else "📭 У вас нет заказов")
        else:
            for order in orders:
                product_id = order['product']
                product = requests.get(BASE_URL + f'/products/{product_id}').json()
                status_icon = "✅" if order['yakunlandi'] else "⏳"
                date = datetime.fromisoformat(order['date'])
                date = str(date.strftime("%Y-%m-%d")) + " " + str(date.strftime("%H:%M:%S"))
                if order['yakunlandi']==False:
                    keyboard = InlineKeyboardMarkup(row_width=1)
                    cancel = InlineKeyboardButton("🚫 Bekor qilish" if lan=='uz' else "🚫 Отмена", callback_data='cancel_order_from_order='+str(order['id']))
                    keyboard.insert(cancel)
                if lan=='uz':
                    order_message = f"...... {status_icon} \n📦 Buyurtma : {product['name_uz']}\n" \
                                    f"🔢 Soni : {order['count']}\n" \
                                    f"💰 Narxi (donasi) : {product['sotish_narx']}\n" \
                                    f"💰 Narxi (umumiy) : {product['sotish_narx']*order['count']}\n" \
                                    f"📍 Manzil : {order['location']}\n" \
                                    f"📞 Tel : {order['tel']}\n" \
                                    f"🗓️ Vaqt : {date}"
                else:
                    order_message = f"...... {status_icon} \n📦 Заказ : {product['name_ru']}\n" \
                                    f"🔢 Число : {order['count']}\n" \
                                    f"💰 Цена (шт.) : {product['sotish_narx']}\n" \
                                    f"💰 Цена (всего) : {product['sotish_narx']*order['count']}\n" \
                                    f"📍 Адрес : {order['location']}\n" \
                                    f"📞 Номер : {order['tel']}\n" \
                                    f"🗓️ Время : {date}"
                if order['yakunlandi']==False: await message.answer(order_message, reply_markup=keyboard)
                else: await message.answer(order_message)
    else:
        await message.answer("⚠️ Buyurtmalarni olishda xatolik yuz berdi" if lan == 'uz' else "⚠️ При получении заказов произошла ошибка")


# Savat
@dp.message_handler(lambda message: message.text in ["🛒 Savat", "🛒 Корзина"])
async def handle_savat(message: types.Message):
    user_id = message.from_user.id
    lan = get_user_language(user_id)
    
    # Make a request to retrieve the user's savat
    api_url = BASE_URL + f'/savat-list/{user_id}/'
    response = requests.get(api_url)
    savats = response.json()
    
    if response.status_code == 200:
        if not savats:
            await message.answer("🛒 Sizning savatingiz bo'sh" if lan=='uz' else "🛒 Ваша корзина пуста")
        else:
            for savat in savats:
                product_id = savat['product']
                product = requests.get(BASE_URL + f'/products/{product_id}').json()
                date = datetime.fromisoformat(savat['date'])
                date = str(date.strftime("%Y-%m-%d")) + " " + str(date.strftime("%H:%M:%S"))
                if lan=='uz':
                    savat_message = f"🛒 Mahsulot : {product['name_uz']}\n" \
                                    f"🔢 Soni : {savat['count']}\n" \
                                    f"💰 Narxi (donasi) : {product['sotish_narx']}\n" \
                                    f"💰 Narxi (umumiy) : {product['sotish_narx']*savat['count']}\n" \
                                    f"📍 Manzil : {savat['location']}\n" \
                                    f"📞 Tel : {savat['tel']}\n" \
                                    f"🗓️ Vaqt : {date}"
                else:
                    savat_message = f"🛒 Продукт : {product['name_ru']}\n" \
                                    f"🔢 Число : {savat['count']}\n" \
                                    f"💰 Цена (шт.) : {product['sotish_narx']}\n" \
                                    f"💰 Цена (всего) : {product['sotish_narx']*savat['count']}\n" \
                                    f"📍 Адрес : {savat['location']}\n" \
                                    f"📞 Номер : {savat['tel']}\n" \
                                    f"🗓️ Время : {date}"
                keyboard = InlineKeyboardMarkup(row_width=2)
                buyurtma_button = InlineKeyboardButton('🚚 Buyurtma berish' if lan=='uz' else "🚚 Разместить заказ", callback_data='add_order_from_savat='+str(savat['id']))
                keyboard.insert(buyurtma_button)
                cancel = InlineKeyboardButton("🚫 Bekor qilish" if lan=='uz' else "🚫 Отмена", callback_data='cancel_order_from_savat='+str(savat['id']))
                keyboard.insert(cancel)
                await message.answer(savat_message, reply_markup=keyboard)
    else:
        await message.answer("⚠️ Savatingiz ma'lumotlarini olishda xatolik yuz berdi" if lan == 'uz' else "⚠️ Произошла ошибка при получении информации о вашей корзине")


@dp.callback_query_handler(lambda query: query.data.startswith("add_order_from_savat"))
async def handle_add_order_from_savat(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lan = get_user_language(user_id)
    order_id = callback_query.data.replace('add_order_from_savat=', '')
    response = requests.get(BASE_URL + '/savat/' + order_id)
    if response.status_code==200:
        savat = response.json()
        api_url = BASE_URL+"/buyurtma/"
        payload = {
            "product": savat['product'],
            "count": savat['count'],
            "location": savat['location'],
            "tel": savat['tel'],
            "user": user_id
        }
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 201:
            requests.delete(BASE_URL + '/savat/' + order_id)
            message = "✅ Buyurtmangiz muvaffaqiyatli amalga oshirildi. Siz bilan tez orada aloqaga chiqamiz." if lan=='uz' else "✅ Ваш заказ успешно выполнен. Мы свяжемся с вами в ближайшее время."
        else: message = "⚠️ Xatolik yuz berdi" if lan == 'uz' else "⚠️ Произошла ошибка"
    else: message = "⚠️ Xatolik yuz berdi" if lan == 'uz' else "⚠️ Произошла ошибка"
    await bot.send_message(chat_id=user_id, text=message)

    

@dp.callback_query_handler(lambda query: query.data.startswith("cancel_order_from_savat"))
async def handle_cancel_order_from_savat(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lan = get_user_language(user_id)
    order_id = callback_query.data.replace('cancel_order_from_savat=', '')
    response = requests.delete(BASE_URL + '/savat/' + order_id)

    if response.status_code == 204: message = "✅ Muvaffaqiyatli bekor qilindi." if lan == 'uz' else "✅ Отменено успешно."
    else: message = "🚫 Xatolik yuz berdi." if lan == 'uz' else "🚫 Произошла ошибка."
    
    await bot.send_message(chat_id=user_id, text=message)


@dp.callback_query_handler(lambda query: query.data.startswith("cancel_order_from_order"))
async def handle_cancel_order_from_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lan = get_user_language(user_id)
    order_id = callback_query.data.replace('cancel_order_from_order=', '')
    response = requests.delete(BASE_URL + '/buyurtma/' + order_id)

    if response.status_code == 204: message = "✅ Muvaffaqiyatli bekor qilindi." if lan == 'uz' else "✅ Отменено успешно."
    else: message = "🚫 Xatolik yuz berdi." if lan == 'uz' else "🚫 Произошла ошибка."
    
    await bot.send_message(chat_id=user_id, text=message)


# find_products
@dp.message_handler(lambda message: message.text.isdigit())
async def find_product(message: types.Message):
    url = BASE_URL+f"/products/?shtrix={message.text}"
    user_id = message.from_user.id
    lan = get_user_language(user_id)
    response = requests.get(url)

    if response.status_code == 200:
        products = response.json()

        if products:
            for product in products['results']:
                if lan=='uz':
                    product_details = f"<b>✅ Brendi:</b> {product['brend']}\n" \
                                    f"<b>✅ Nomi:</b> {product['name_uz']}\n" \
                                    f"<b>✅ Narxi:</b> ${product['sotish_narx']}\n"
                else:
                    product_details = f"<b>✅ Бренд:</b> {product['brend']}\n" \
                                    f"<b>✅ Наименование:</b> {product['name_ru']}\n" \
                                    f"<b>✅ Цена:</b> ${product['sotish_narx']}\n"
                if product['xarakteristika_uz']:
                    if lan=='uz': product_details += f"<b>✅ Xarakteristikasi:</b>\n{bleach.clean(product['xarakteristika_uz'], tags=[], attributes={}, strip=True)}"
                    else: product_details += f"<b>✅ Характеристика:</b>\n{bleach.clean(product['xarakteristika_ru'], tags=[], attributes={}, strip=True)}"
                add_keyboard = InlineKeyboardMarkup(row_width=2)
                buyurtma_button = InlineKeyboardButton('🚚 Buyurtma berish' if lan=='uz' else "🚚 Разместить заказ", callback_data='add_buyurtma='+str(product['id']))
                add_keyboard.insert(buyurtma_button)
                savat_button = InlineKeyboardButton("🛒 Savatga qo'shish" if lan=='uz' else "🛒 В корзину", callback_data='add_savat='+str(product['id']))
                add_keyboard.insert(savat_button)
                if product['image']:
                    await bot.send_photo(message.chat.id, photo=product['image'], caption=product_details, parse_mode='HTML', reply_markup=add_keyboard)
                else:
                    await message.answer(product_details, parse_mode="HTML", reply_markup=add_keyboard)
        else:
            await message.reply("No products found with the specified shtirx value.")
    else:
        await message.reply("An error occurred while retrieving the products.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)