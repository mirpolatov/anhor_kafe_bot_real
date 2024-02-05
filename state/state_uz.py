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


class Delete(StatesGroup):
    food_name = State()


class Form(StatesGroup):
    food_name = State()
    amount = State()


class Suv(StatesGroup):
    ichimlik_name = State()
    ichimlik_amount = State()


class Calat(StatesGroup):
    salat_name = State()
    salat_amount = State()
