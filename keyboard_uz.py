from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_button = [
    [KeyboardButton(text='🇺🇿 Uzbek'),
     KeyboardButton(text='🇷🇺 Russia'),
     ],
]

language = ReplyKeyboardMarkup(keyboard=keyboard_button, resize_keyboard=True, row_width=1)
