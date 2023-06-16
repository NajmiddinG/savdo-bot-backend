from aiogram.dispatcher.filters.state import State, StatesGroup

class OrderState(StatesGroup):
    quantity = State()
    location = State()
    phone_number = State()
    product_id = State()

class CartState(StatesGroup):
    quantity = State()
    location = State()
    phone_number = State()
    product_id = State()