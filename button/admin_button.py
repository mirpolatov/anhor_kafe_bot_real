from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)


def main_rp():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Maxsulot qo'shish")
    movies = KeyboardButton("Maxsulot ko'rish")
    return btn.add(statistika, movies)


def food_delete():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("Delete", callback_data='delete'))
    ikm.add(InlineKeyboardButton("Tahrirlash", callback_data='tahrirlash'))
    ikm.add(InlineKeyboardButton("Bekor qilish", callback_data='bekor'))
    return ikm


def food():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("✖")
    return btn.add(statistika)
