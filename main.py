import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from admin_button import main_rp, admin, ichimlik, salat, food_delete
from db import Session, FoodItem, Ichimliklar, Salat

from keyboard_uz import language
from state import Forms, Ichimlik, Salatlar

Token = '6749635309:AAEUCc1S6K3znbNXqfFqydAAkfhNLquE4hk'

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

session = Session()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id != 5772722670:
        await message.answer("Тилни танланг  /   Выберите язык", reply_markup=language)
    else:
        await message.answer("hello bro", reply_markup=admin())


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(text='Bizda bunday buyruq mavjud emas.   /    У нас нет такого приказа.', reply=message.text)

'''----------------------------Ovqatlar-----------------------------------'''


@dp.message_handler(lambda message: message.text == "Ovqatlar")
async def start_food_registration(message: types.Message):
    await message.answer('hello world', reply_markup=main_rp())


@dp.message_handler(lambda message: message.text == "Ovqat qo'shish")
async def start_food_registration(message: types.Message):
    await message.answer("Iltimos,ovqat rasmini kiriting.")
    await Forms.food_picture.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Forms.food_picture)
async def process_food_picture(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['food_picture'] = photo_id

    await Forms.next()
    await message.answer("Iltimos,ovqat nomini kiriting:")


@dp.message_handler(state=Forms.food_name)
async def process_food_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['food_name'] = message.text

    await Forms.next()
    await message.answer("Iltimos, summasni kiriting:")


@dp.message_handler(state=Forms.amount)
async def process_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text

        file_id = data['food_picture']
        file = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file.file_path)

        db = Session()
        food = FoodItem(
            food_picture=downloaded_file.read(),
            food_name=data['food_name'],
            amount=data['amount']
        )
        db.add(food)
        db.commit()

        await state.finish()
        await message.answer(
            f"Ovqat nomi '{data['food_name']}'  Ovqat summasi {data['amount']} malumotlar saqlandi."
        )


async def food_info(message: types.Message):
    db = Session()
    food_items = db.query(FoodItem).all()
    db.close()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for food_item in food_items:
        button_text = f"{food_item.food_name}"
        keyboard.add(types.KeyboardButton(text=button_text))

    await bot.send_message(chat_id=message.chat.id, text="Mavjud ovqatlar:", reply_markup=keyboard)


@dp.message_handler(
    lambda message: any(food_item.food_name in message.text for food_item in Session().query(FoodItem).all()))
async def show_food_details(message: types.Message):
    db = Session()
    selected_food_name = next(
        (food_item.food_name for food_item in db.query(FoodItem).all() if food_item.food_name in message.text), None)
    if selected_food_name:
        try:

            selected_food_item = db.query(FoodItem).filter(FoodItem.food_name == selected_food_name).first()

            photo = selected_food_item.food_picture
            details_text = f" Ovqat raqami : {selected_food_item.id}\nOvqat nomi: {selected_food_item.food_name}\nOvqat summasi: {selected_food_item.amount}"
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=details_text,
                                 reply_markup=food_delete())
        finally:
            db.close()


@dp.message_handler(lambda message: message.text == "Ovqatlarni ko'rish")
async def start_food_registration(message: types.Message):
    await food_info(message)


"""--------------------------ichimliklar------------------------"""


@dp.message_handler(lambda message: message.text == "Ichimliklar")
async def start_food_registration(message: types.Message):
    await message.answer('hello world', reply_markup=ichimlik())


@dp.message_handler(lambda message: message.text == "Ichimlikar qo'shish")
async def start_food_registration(message: types.Message):
    await message.answer("Iltimos,ichimlik rasmini kiriting.")
    await Ichimlik.picture.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Ichimlik.picture)
async def process_food_picture(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['picture'] = photo_id

    await Ichimlik.next()
    await message.answer("Iltimos,ichimlik nomini kiriting:")


@dp.message_handler(state=Ichimlik.name)
async def process_food_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Ichimlik.next()
    await message.answer("Iltimos, summasni kiriting:")


@dp.message_handler(state=Ichimlik.amount)
async def process_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text

        file_id = data['picture']
        file = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file.file_path)

        db = Session()
        food = Ichimliklar(
            ichimlik_picture=downloaded_file.read(),
            ichimlik_name=data['name'],
            ichimlik_amount=data['amount']
        )
        db.add(food)
        db.commit()

        await state.finish()
        await message.answer('Tabriklaymiz maxsulot qo''shildi'
                             )


async def ichimlik_info(message: types.Message):
    db = Session()
    food_items = db.query(Ichimliklar).all()
    db.close()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for food_item in food_items:
        button_text = f"{food_item.ichimlik_name}"
        keyboard.add(types.KeyboardButton(text=button_text))

    await bot.send_message(chat_id=message.chat.id, text="Mavjud ichimliklar:", reply_markup=keyboard)


@dp.message_handler(
    lambda message: any(food_item.ichimlik_name in message.text for food_item in Session().query(Ichimliklar).all()))
async def show_food_details(message: types.Message):
    db = Session()
    selected_food_name = next(
        (food_item.ichimlik_name for food_item in db.query(Ichimliklar).all() if
         food_item.ichimlik_name in message.text), None)
    if selected_food_name:
        try:

            selected_food_item = db.query(Ichimliklar).filter(Ichimliklar.ichimlik_name == selected_food_name).first()

            photo = selected_food_item.ichimlik_picture
            details_text = f" Ichimlik raqami : {selected_food_item.id}\nIchimlik nomi: {selected_food_item.ichimlik_name}\nIchimlik summasi: {selected_food_item.ichimlik_amount}"
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=details_text,
                                 reply_markup=food_delete())
        finally:
            db.close()


@dp.message_handler(lambda message: message.text == "Ichimlikarni ko'rish")
async def start_food_registration(message: types.Message):
    await ichimlik_info(message)


'''------------------------Salatlar------------------------'''


@dp.message_handler(lambda message: message.text == "Salatlar")
async def start_food_registration(message: types.Message):
    await message.answer('hello world', reply_markup=salat())


@dp.message_handler(lambda message: message.text == "Salat qo'shish")
async def start_food_registration(message: types.Message):
    await message.answer("Iltimos,salat rasmini kiriting.")
    await Salatlar.picture.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Salatlar.picture)
async def process_food_picture(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['picture'] = photo_id

    await Salatlar.next()
    await message.answer("Iltimos,salat nomini kiriting:")


@dp.message_handler(state=Salatlar.name)
async def process_food_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Salatlar.next()
    await message.answer("Iltimos, summasni kiriting:")


@dp.message_handler(state=Salatlar.amount)
async def process_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text

        file_id = data['picture']
        file = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file.file_path)

        db = Session()
        food = Salat(
            salat_picture=downloaded_file.read(),
            salat_name=data['name'],
            salat_amount=data['amount']
        )
        db.add(food)
        db.commit()

        await state.finish()
        await message.answer('Tabriklaymiz maxsulot qo''shildi'
                             )


async def salat_info(message: types.Message):
    db = Session()
    food_items = db.query(Salat).all()
    db.close()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for food_item in food_items:
        button_text = f"{food_item.salat_name}"
        keyboard.add(types.KeyboardButton(text=button_text))

    await bot.send_message(chat_id=message.chat.id, text="Mavjud salatlar:", reply_markup=keyboard)


@dp.message_handler(
    lambda message: any(food_item.salat_name in message.text for food_item in Session().query(Salat).all()))
async def show_food_details(message: types.Message):
    db = Session()
    selected_food_name = next(
        (food_item.salat_name for food_item in db.query(Salat).all() if
         food_item.salat_name in message.text), None)
    if selected_food_name:
        try:

            selected_food_item = db.query(Salat).filter(Salat.salat_name == selected_food_name).first()

            photo = selected_food_item.salat_picture
            details_text = f" Salat raqami : {selected_food_item.id}\nSalat nomi: {selected_food_item.salat_name}\nSalat summasi: {selected_food_item.salat_amount}"
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=details_text,
                                 reply_markup=food_delete())
        finally:
            db.close()


@dp.message_handler(lambda message: message.text == "Salatlarni ko'rish")
async def start_food_registration(message: types.Message):
    await salat_info(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
