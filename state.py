from aiogram.dispatcher.filters.state import StatesGroup, State


class Forms(StatesGroup):
    food_picture = State()
    food_name = State()
    amount = State()


class Ichimlik(StatesGroup):
    picture = State()
    name = State()
    amount = State()


class Salatlar(StatesGroup):
    picture = State()
    name = State()
    amount = State()
