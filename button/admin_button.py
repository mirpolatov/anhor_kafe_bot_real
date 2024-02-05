from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)


def Til():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("UZ🇺🇿", callback_data='uzbek'))
    ikm.add(InlineKeyboardButton("Rus🇷🇺", callback_data='russia'))
    ikm.add(InlineKeyboardButton("Kril", callback_data='kril'))
    return ikm


def main_rp():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Ovqat qo'shish")
    movies = KeyboardButton("Ovqatlarni ko'rish")
    menu = KeyboardButton("⏮Orqaga")
    return btn.add(statistika, movies, menu)


def salat():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Salat qo'shish")
    movies = KeyboardButton("Salatlarni ko'rish")

    menu = KeyboardButton("⏮Orqaga")
    return btn.add(statistika, movies, menu)


def ichimlik():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Ichimlikar qo'shish")
    movies = KeyboardButton("Ichimlikarni ko'rish")
    menu = KeyboardButton("⏮Orqaga")
    return btn.add(statistika, movies, menu)


def admin():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Ovqatlar")
    movies = KeyboardButton("Ichimliklar")
    reklama = KeyboardButton("Salatlar")
    return btn.add(statistika, movies, reklama)


def food_delete():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("Delete", callback_data='delete'))
    ikm.add(InlineKeyboardButton("Tahrirlash", callback_data='tahrirlash'))
    ikm.add(InlineKeyboardButton("Bekor qilish", callback_data='bekor'))
    return ikm


def Water_delete():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("Delete🌊", callback_data='delete🌊'))
    ikm.add(InlineKeyboardButton("Tahrirlash🌊", callback_data='tahrirlash🌊'))
    ikm.add(InlineKeyboardButton("Bekor qilish🌊", callback_data='bekor🌊'))
    return ikm


def Salat_delete():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("Delete🥗", callback_data='delete🥗'))
    ikm.add(InlineKeyboardButton("Tahrirlash🥗", callback_data='tahrirlash🥗'))
    ikm.add(InlineKeyboardButton("Bekor qilish🥗", callback_data='bekor🥗'))
    return ikm


def food():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("✖")
    return btn.add(statistika)
