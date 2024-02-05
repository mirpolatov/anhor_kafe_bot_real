from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)


def main_ru():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Добавление еды")
    movies = KeyboardButton("Посмотреть продукты")
    menu = KeyboardButton("⏮Назад")
    return btn.add(statistika, movies, menu)


def salat_ru():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Добавить салат")
    movies = KeyboardButton("Посмотреть салаты")

    menu = KeyboardButton("⏮Назад")
    return btn.add(statistika, movies, menu)


def ichimlik_ru():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Добавьте газированные напитки")
    movies = KeyboardButton("Посмотреть газированные напитки")
    menu = KeyboardButton("⏮Назад")
    return btn.add(statistika, movies, menu)


def admin_ru():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("Питание")
    movies = KeyboardButton("Напитки")
    reklama = KeyboardButton("Салаты")
    return btn.add(statistika, movies, reklama)


def food_delete_ru():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("Удалить", callback_data='yдалить'))
    ikm.add(InlineKeyboardButton("Изменять", callback_data='изменять'))
    ikm.add(InlineKeyboardButton("Отмена", callback_data='oтмена'))
    return ikm


def Water_delete_ru():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("Удалить🌊", callback_data='yдалить🌊'))
    ikm.add(InlineKeyboardButton("Изменять🌊", callback_data='изменять🌊'))
    ikm.add(InlineKeyboardButton("Отмена🌊", callback_data='oтмена🌊'))
    return ikm


def Salat_delete_ru():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("Удалить🥗", callback_data='yдалить🥗'))
    ikm.add(InlineKeyboardButton("Изменять🥗", callback_data='изменять🥗'))
    ikm.add(InlineKeyboardButton("Отмена🥗", callback_data='oтмена🥗'))
    return ikm


def food_ru():
    btn = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    statistika = KeyboardButton("✖")
    return btn.add(statistika)
