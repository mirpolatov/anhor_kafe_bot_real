from aiogram.dispatcher.filters.state import StatesGroup, State


class Forms_ru(StatesGroup):
    food_picture = State()
    food_name = State()
    amount = State()


class Ichimlik_ru(StatesGroup):
    picture = State()
    name = State()
    amount = State()


class Salatlar_ru(StatesGroup):
    picture = State()
    name = State()
    amount = State()


class Delete_ru(StatesGroup):
    food_name = State()


class Form_ru(StatesGroup):
    food_name = State()
    amount = State()


class Suv_ru(StatesGroup):
    ichimlik_name = State()
    ichimlik_amount = State()


class Calat_ru(StatesGroup):
    salat_name = State()
    salat_amount = State()
