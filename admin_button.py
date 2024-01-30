from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)


def main_rp():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Ovqat qo'shish")
    movies = KeyboardButton("Ovqatlarni ko'rish")
    reklama = KeyboardButton("Ovqatlarni narxini o'zgartirish")
    menu = KeyboardButton("Menu🖇")
    return btn.add(statistika, movies, reklama, menu)


def salat():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Salat qo'shish")
    movies = KeyboardButton("Salatlarni ko'rish")
    reklama = KeyboardButton("Salatni narxini o'zgartirish")
    menu = KeyboardButton("Menu⛔")
    return btn.add(statistika, movies, reklama, menu)


def ichimlik():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Ichimlikar qo'shish")
    movies = KeyboardButton("Ichimlikarni ko'rish")
    reklama = KeyboardButton("Ichimlik narxini o'zgartirish")
    menu = KeyboardButton("Menu🛠")
    return btn.add(statistika, movies, reklama, menu)


def admin():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Ovqatlar")
    movies = KeyboardButton("Ichimliklar")
    reklama = KeyboardButton("Salatlar")
    return btn.add(statistika, movies, reklama)


def food_delete():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("Delete", callback_data='delete'))
    ikm.add(InlineKeyboardButton("Bekor qilish", callback_data='bekor'))
    return ikm
