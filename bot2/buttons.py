from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_keyboard_markup(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, 
                                    keyboard=[
                                        [
                                        KeyboardButton(text="🛠 Mahsulotlar" if language == "uz" else "🛠 Продукты"),
                                        KeyboardButton(text="🛒 Savat" if language == "uz" else "🛒 Корзина"),
                                        ],
                                        [
                                        KeyboardButton(text="🚚 Buyurtmalar" if language == "uz" else "🚚 Заказы"),
                                        KeyboardButton(text="🇺🇿 Tilni o'zgartirish" if language == "uz" else "🇷🇺 Изменить язык"),
                                        ],
                                        [
                                        KeyboardButton(text="❓ Yordam" if language == "uz" else "❓ Помощь"),
                                        KeyboardButton(text="☎️ Bog'lanish" if language == "uz" else "☎️ Связь"),
                                        ]
                                    ])
    return button