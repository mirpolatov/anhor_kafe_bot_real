from aiogram.dispatcher.filters.state import StatesGroup, State


class Forms(StatesGroup):
    food_picture = State()
    food_name = State()
    amount = State()


class Delete(StatesGroup):
    food_name = State()


class Form(StatesGroup):
    food_name = State()
    amount = State()
