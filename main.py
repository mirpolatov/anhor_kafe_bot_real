from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from button.admin_button import main_rp, admin, ichimlik, salat, Water_delete, Salat_delete, Til, food_delete, food
from button.admin_button_ru import admin_ru, main_ru, food_ru, food_delete_ru, ichimlik_ru, Water_delete_ru, salat_ru, \
    Salat_delete_ru
from db import Session, FoodItem, Ichimliklar, Salat, FoodItemRu, IchimliklarRu, SalatRu
from funksiyalar.funksiya1 import get_selected_food_name, get_selected_ichimlik_name, get_selected_salat_name
from funksiyalar.funksiya_ru import get_selected_food_name_ru, get_selected_ichimlik_name_ru, get_selected_salat_name_ru

from keyboard_uz import language
from state.state_ru import Forms_ru, Form_ru, Ichimlik_ru, Suv_ru, Salatlar_ru, Calat_ru
from state.state_uz import Ichimlik, Salatlar, Form, Suv, Calat, Forms

Token = '6749635309:AAG3QgYt9vekUnKbyhQzISlSe2CMIWnWRDs'

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

session = Session()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id != 5161994540 and message.from_user.id != 1930798399 and message.from_user.id != 5772722670:
        await message.answer("Тилни танланг  /   Выберите язык", reply_markup=language)
    else:
        await message.answer("hello bro", reply_markup=Til())


'''-----------------------UZ------------------------'''


@dp.callback_query_handler(lambda query: query.data == 'uzbek')
async def process_order(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, "Menu :", reply_markup=admin())
    chat_id = query.message.chat.id
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


'''----------------------------Ovqatlar-----------------------------------'''


@dp.message_handler(lambda message: message.text == "Ovqatlar")
async def start_food_registration(message: types.Message):
    await message.answer('hello world', reply_markup=main_rp())


@dp.message_handler(lambda message: message.text == "Ovqat qo'shish")
async def start_food_registration(message: types.Message):
    await message.answer("Iltimos,ovqat rasmini kiriting.")
    await Forms.food_picture.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Forms.food_picture)
async def process_food_picture(message: types.Message, state: FSMContext, ):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        if message.text == "✖":
            await state.finish()
            await message.answer('Amal bekor qilindi.', reply_markup=main_rp())
            return
        data['food_picture'] = photo_id

    await Forms.next()
    await message.answer("Iltimos,ovqat nomini kiriting:", reply_markup=food())


@dp.message_handler(state=Forms.food_name)
async def process_food_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "✖":
            await state.finish()
            await message.answer('Amal bekor qilindi.', reply_markup=main_rp())
            return
        data['food_name'] = message.text

    await Forms.next()
    await message.answer("Iltimos, summasni kiriting:")


@dp.message_handler(state=Forms.amount)
async def process_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "✖":
            await state.finish()
            await message.answer('Amal bekor qilindi.', reply_markup=main_rp())
            return
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
            'Tabriklaymiz maxsulot qo''shildi'
        )


async def food_info(message: types.Message):
    db = Session()
    food_items = db.query(FoodItem).all()
    db.close()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for food_item in food_items:
        button_text = f"{food_item.food_name}"
        keyboard.add(types.KeyboardButton(text=button_text))

    delete_button = types.KeyboardButton(text="🔙Orqaga")
    keyboard.add(delete_button)

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


@dp.message_handler(lambda message: message.text == "✖")
async def start_food_registration(message: types.Message):
    await message.answer('hello word', reply_markup=main_rp())


@dp.message_handler(lambda message: message.text == "🔙Orqaga")
async def start_food_registration(message: types.Message):
    await message.answer('Mavjud ovqatlar:', reply_markup=main_rp())


from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda query: query.data == 'delete', state="*")
async def process_delete(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    selected_food_name = get_selected_food_name()
    async with state.proxy() as data:
        data['food_name'] = selected_food_name

        if selected_food_name:
            db = Session()
            food_item = db.query(FoodItem).filter_by(food_name=selected_food_name).first()
            if food_item:
                food_item.food_name = selected_food_name
                db.delete(food_item)
                db.commit()
            db.close()
            chat_id = query.message.chat.id

            await bot.send_message(chat_id=chat_id, text='✅ Malumotlarni o\'chirildi')

            data.clear()
            message_id = query.message.message_id

            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        else:

            await bot.answer_callback_query(query.id, text='❌ Ma\'lumot topilmadi')


@dp.callback_query_handler(lambda query: query.data == 'tahrirlash', state='*')
async def process_order(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    selected_food_name = get_selected_food_name()

    async with state.proxy() as data:
        data['food_name'] = selected_food_name

    await Form.amount.set()
    await query.message.answer("Iltimos o'zgartirilgan narxni kiriting")


@dp.message_handler(state=Form.amount)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
        ordered_food_name = data['food_name']
        product = session.query(FoodItem).filter_by(food_name=ordered_food_name).first()

        if product:

            product.amount = data['amount']

            session.commit()

            await message.answer('O\'zgardi')

        else:
            await message.answer('O\'zgarmadi')

    await state.finish()


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
    delete_button = types.KeyboardButton(text="⏪Orqaga")
    keyboard.add(delete_button)

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
                                 reply_markup=Water_delete())
        finally:
            db.close()


@dp.message_handler(lambda message: message.text == "Ichimlikarni ko'rish")
async def start_food_registration(message: types.Message):
    await ichimlik_info(message)


@dp.message_handler(lambda message: message.text == "⏪Orqaga")
async def start_food_registration(message: types.Message):
    await message.answer('Menu:', reply_markup=ichimlik())


@dp.callback_query_handler(lambda query: query.data == 'delete🌊', state="*")
async def process_delete(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    selected_ichimlik_name = get_selected_ichimlik_name()
    async with state.proxy() as data:
        data['ichimlik_name'] = selected_ichimlik_name

        if selected_ichimlik_name:
            db = Session()
            food_item = db.query(Ichimliklar).filter_by(ichimlik_name=selected_ichimlik_name).first()
            if food_item:
                food_item.ichimlik_name = selected_ichimlik_name
                db.delete(food_item)
                db.commit()
            db.close()
            chat_id = query.message.chat.id

            await bot.send_message(chat_id=chat_id, text='✅ Malumotlarni o\'chirildi')

            data.clear()
            message_id = query.message.message_id

            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        else:

            await bot.answer_callback_query(query.id, text='❌ Ma\'lumot topilmadi')


@dp.callback_query_handler(lambda query: query.data == 'tahrirlash🌊', state='*')
async def process_order(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    selected_food_name = get_selected_ichimlik_name()

    async with state.proxy() as data:
        data['ichimlik_name'] = selected_food_name

    await Suv.ichimlik_amount.set()
    await query.message.answer("Iltimos o'zgartirilgan narxni kiriting")


@dp.message_handler(state=Suv.ichimlik_amount)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ichimlik_amount'] = message.text
        ordered_food_name = data['ichimlik_name']
        product = session.query(Ichimliklar).filter_by(ichimlik_name=ordered_food_name).first()

        if product:

            product.ichimlik_amount = data['ichimlik_amount']

            session.commit()

            await message.answer('O\'zgardi')

        else:
            await message.answer('O\'zgarmadi')

    await state.finish()


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
    delete_button = types.KeyboardButton(text="⬅Orqaga")
    keyboard.add(delete_button)

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
                                 reply_markup=Salat_delete())
        finally:
            db.close()


@dp.message_handler(lambda message: message.text == "Salatlarni ko'rish")
async def start_food_registration(message: types.Message):
    await salat_info(message)


@dp.message_handler(lambda message: message.text == "Salatlarni ko'rish")
async def start_food_registration(message: types.Message):
    await salat_info(message)


@dp.callback_query_handler(lambda query: query.data == 'delete🥗', state="*")
async def process_delete(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    salat_name = get_selected_salat_name()
    async with state.proxy() as data:
        data['salat_name'] = salat_name

        if salat_name:
            db = Session()
            food_item = db.query(Salat).filter_by(salat_name=salat_name).first()
            if food_item:
                food_item.salat_name = salat_name
                db.delete(food_item)
                db.commit()
            db.close()
            chat_id = query.message.chat.id

            await bot.send_message(chat_id=chat_id, text='✅ Malumotlarni o\'chirildi')

            data.clear()
            message_id = query.message.message_id

            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        else:

            await bot.answer_callback_query(query.id, text='❌ Ma\'lumot topilmadi')


@dp.callback_query_handler(lambda query: query.data == 'tahrirlash🥗', state='*')
async def process_order(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    selected_food_name = get_selected_salat_name()

    async with state.proxy() as data:
        data['salat_name'] = selected_food_name

    await Calat.salat_amount.set()
    await query.message.answer("Iltimos o'zgartirilgan narxni kiriting")


@dp.message_handler(state=Calat.salat_amount)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['salat_amount'] = message.text
        ordered_food_name = data['salat_name']
        product = session.query(Salat).filter_by(salat_name=ordered_food_name).first()

        if product:

            product.salat_amount = data['salat_amount']

            session.commit()

            await message.answer('O\'zgardi')

        else:
            await message.answer('O\'zgarmadi')

    await state.finish()


'''--------------------------------------------------------------------------'''


@dp.callback_query_handler(lambda query: query.data == 'bekor')
async def delete_message(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    await bot.answer_callback_query(query.id, '✅ Malumotlarni o''chirish bekor qilindi ')
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


@dp.message_handler(lambda message: message.text == "⏮Orqaga")
async def start_food_registration(message: types.Message):
    await message.answer('hello bro', reply_markup=admin())


@dp.message_handler(lambda message: message.text == "✖")
async def start_food_registration(message: types.Message):
    await message.answer('hello word', reply_markup=main_rp())


@dp.message_handler(lambda message: message.text == "⬅Orqaga")
async def start_food_registration(message: types.Message):
    await message.answer('Menu:', reply_markup=salat())


'''---------------------------------------------------'''

'''---------------------------RUS---------------------------'''


@dp.callback_query_handler(lambda query: query.data == 'russia')
async def process_order(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, "Меню :", reply_markup=admin_ru())
    chat_id = query.message.chat.id
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


'''----------------------------Ovqatlar-----------------------------------'''


@dp.message_handler(lambda message: message.text == "Питание")
async def start_food_registration(message: types.Message):
    await message.answer('Привет', reply_markup=main_ru())


@dp.message_handler(lambda message: message.text == "Добавление еды")
async def start_food_registration(message: types.Message):
    await message.answer("Пожалуйста, вставьте изображение еды.", reply_markup=food_ru())
    await Forms_ru.food_picture.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Forms_ru.food_picture)
async def process_food_picture(message: types.Message, state: FSMContext, ):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        if message.text == "❌":
            await state.finish()
            await message.answer('Действие отменено.', reply_markup=main_ru())
            return
        data['food_picture'] = photo_id

    await Forms_ru.next()
    await message.answer("Пожалуйста, введите название блюда:")


@dp.message_handler(state=Forms_ru.food_name)
async def process_food_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "❌":
            await state.finish()
            await message.answer('Действие отменено.', reply_markup=main_ru())
            return
        data['food_name'] = message.text

    await Forms_ru.next()
    await message.answer("Пожалуйста, введите сумму:")


@dp.message_handler(state=Forms_ru.amount)
async def process_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "❌":
            await state.finish()
            await message.answer('Действие отменено.', reply_markup=main_ru())
            return
        data['amount'] = message.text

        file_id = data['food_picture']
        file = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file.file_path)

        db = Session()
        food = FoodItemRu(
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


async def food_info_ru(message: types.Message):
    db = Session()
    food_items = db.query(FoodItemRu).all()
    db.close()

    keyboard_ru = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for food_item in food_items:
        button_text = f"{food_item.food_name}"
        keyboard_ru.add(types.KeyboardButton(text=button_text))

    delete_button = types.KeyboardButton(text="🔙Назад")
    keyboard_ru.add(delete_button)

    await bot.send_message(chat_id=message.chat.id, text="Доступные продукты:", reply_markup=keyboard_ru)


@dp.message_handler(
    lambda message: any(food_item.food_name in message.text for food_item in Session().query(FoodItemRu).all()))
async def show_food_details(message: types.Message):
    db = Session()
    selected_food_name = next(
        (food_item.food_name for food_item in db.query(FoodItemRu).all() if food_item.food_name in message.text), None)
    if selected_food_name:
        try:

            selected_food_item = db.query(FoodItemRu).filter(FoodItemRu.food_name == selected_food_name).first()

            photo = selected_food_item.food_picture
            details_text = f" Номер еды : {selected_food_item.id}\n:Название еды {selected_food_item.food_name}\nЦена еды: {selected_food_item.amount}"
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=details_text,
                                 reply_markup=food_delete_ru())
        finally:
            db.close()


@dp.message_handler(lambda message: message.text == "Посмотреть продукты")
async def start_food_registration(message: types.Message):
    await food_info_ru(message)


@dp.message_handler(lambda message: message.text == "❌")
async def start_food_registration(message: types.Message):
    await message.answer('Привет', reply_markup=main_ru())


@dp.message_handler(lambda message: message.text == "🔙Назад")
async def start_food_registration(message: types.Message):
    await message.answer('Меню:', reply_markup=main_ru())


from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda query: query.data == 'yдалить', state="*")
async def process_delete(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    selected_food_name = get_selected_food_name_ru()
    async with state.proxy() as data:
        data['food_name'] = selected_food_name

        if selected_food_name:
            db = Session()
            food_item = db.query(FoodItemRu).filter_by(food_name=selected_food_name).first()
            if food_item:
                food_item.food_name = selected_food_name
                db.delete(food_item)
                db.commit()
            db.close()
            chat_id = query.message.chat.id

            await bot.send_message(chat_id=chat_id, text='✅ Данные удалены')

            data.clear()
            message_id = query.message.message_id

            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        else:

            await bot.answer_callback_query(query.id, text='❌ Информация не найдена')


@dp.callback_query_handler(lambda query: query.data == 'изменять', state='*')
async def process_order(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    selected_food_name = get_selected_food_name_ru()

    async with state.proxy() as data:
        data['food_name'] = selected_food_name

    await Form_ru.amount.set()
    await query.message.answer("Пожалуйста, введите пересмотренную цену")


@dp.message_handler(state=Form_ru.amount)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
        ordered_food_name = data['food_name']
        product = session.query(FoodItemRu).filter_by(food_name=ordered_food_name).first()

        if product:

            product.amount = data['amount']

            session.commit()

            await message.answer('Информация изменилась')

        else:
            await message.answer('Информация не изменилась')

    await state.finish()


"""--------------------------ichimliklar------------------------"""


@dp.message_handler(lambda message: message.text == "Напитки")
async def start_food_registration(message: types.Message):
    await message.answer('Привет', reply_markup=ichimlik_ru())


@dp.message_handler(lambda message: message.text == "Добавьте газированные напитки")
async def start_food_registration(message: types.Message):
    await message.answer("Пожалуйста, введите изображение напитка.")
    await Ichimlik_ru.picture.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Ichimlik_ru.picture)
async def process_food_picture(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['picture'] = photo_id

    await Ichimlik_ru.next()
    await message.answer("Пожалуйста, введите название напитка:")


@dp.message_handler(state=Ichimlik_ru.name)
async def process_food_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Ichimlik_ru.next()
    await message.answer("Пожалуйста, введите сумму:")


@dp.message_handler(state=Ichimlik_ru.amount)
async def process_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text

        file_id = data['picture']
        file = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file.file_path)

        db = Session()
        food = IchimliklarRu(
            ichimlik_picture=downloaded_file.read(),
            ichimlik_name=data['name'],
            ichimlik_amount=data['amount']
        )
        db.add(food)
        db.commit()

        await state.finish()
        await message.answer('Поздравляем, товар добавлен'
                             )


async def ichimlik_info_ru(message: types.Message):
    db = Session()
    food_items = db.query(IchimliklarRu).all()
    db.close()

    keyboard_rus = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for food_item in food_items:
        button_text = f"{food_item.ichimlik_name}"
        keyboard_rus.add(types.KeyboardButton(text=button_text))
    delete_button = types.KeyboardButton(text="⏪Назад")
    keyboard_rus.add(delete_button)

    await bot.send_message(chat_id=message.chat.id, text="Доступны напитки:", reply_markup=keyboard_rus)


@dp.message_handler(
    lambda message: any(food_item.ichimlik_name in message.text for food_item in Session().query(IchimliklarRu).all()))
async def show_food_details(message: types.Message):
    db = Session()
    selected_food_name = next(
        (food_item.ichimlik_name for food_item in db.query(IchimliklarRu).all() if
         food_item.ichimlik_name in message.text), None)
    if selected_food_name:
        try:

            selected_food_item = db.query(IchimliklarRu).filter(
                IchimliklarRu.ichimlik_name == selected_food_name).first()

            photo = selected_food_item.ichimlik_picture
            details_text = f" Номер напитка : {selected_food_item.id}\nНазвание напитка: {selected_food_item.ichimlik_name}\nЦена напитка: {selected_food_item.ichimlik_amount}"
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=details_text,
                                 reply_markup=Water_delete_ru())
        finally:
            db.close()


@dp.message_handler(lambda message: message.text == "Посмотреть газированные напитки")
async def start_food_registration(message: types.Message):
    await ichimlik_info_ru(message)


@dp.message_handler(lambda message: message.text == "⏪Назад")
async def start_food_registration(message: types.Message):
    await message.answer('Menu:', reply_markup=ichimlik_ru())


@dp.callback_query_handler(lambda query: query.data == 'yдалить🌊', state="*")
async def process_delete(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    selected_ichimlik_name = get_selected_ichimlik_name_ru()
    async with state.proxy() as data:
        data['ichimlik_name'] = selected_ichimlik_name

        if selected_ichimlik_name:
            db = Session()
            food_item = db.query(IchimliklarRu).filter_by(ichimlik_name=selected_ichimlik_name).first()
            if food_item:
                food_item.ichimlik_name = selected_ichimlik_name
                db.delete(food_item)
                db.commit()
            db.close()
            chat_id = query.message.chat.id

            await bot.send_message(chat_id=chat_id, text='✅ Данные удалены')

            data.clear()
            message_id = query.message.message_id

            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        else:

            await bot.answer_callback_query(query.id, text='❌ Информация не найдена')


@dp.callback_query_handler(lambda query: query.data == 'изменять🌊', state='*')
async def process_order(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    selected_food_name = get_selected_ichimlik_name_ru()

    async with state.proxy() as data:
        data['ichimlik_name'] = selected_food_name

    await Suv_ru.ichimlik_amount.set()
    await query.message.answer("Пожалуйста, введите пересмотренную цену")


@dp.message_handler(state=Suv_ru.ichimlik_amount)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ichimlik_amount'] = message.text
        ordered_food_name = data['ichimlik_name']
        product = session.query(IchimliklarRu).filter_by(ichimlik_name=ordered_food_name).first()

        if product:

            product.ichimlik_amount = data['ichimlik_amount']

            session.commit()

            await message.answer('Товар изменился')

        else:
            await message.answer('Товар не изменился')

    await state.finish()


'''------------------------Salatlar------------------------'''


@dp.message_handler(lambda message: message.text == "Салаты")
async def start_food_registration(message: types.Message):
    await message.answer('Привет', reply_markup=salat_ru())


@dp.message_handler(lambda message: message.text == "Добавить салат")
async def start_food_registration(message: types.Message):
    await message.answer("Пожалуйста, введите фотографию салата.")
    await Salatlar_ru.picture.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Salatlar_ru.picture)
async def process_food_picture(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['picture'] = photo_id

    await Salatlar_ru.next()
    await message.answer("Пожалуйста, введите название салата:")


@dp.message_handler(state=Salatlar_ru.name)
async def process_food_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Salatlar_ru.next()
    await message.answer("Пожалуйста, введите цену:")


@dp.message_handler(state=Salatlar_ru.amount)
async def process_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text

        file_id = data['picture']
        file = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file.file_path)

        db = Session()
        food = SalatRu(
            salat_picture=downloaded_file.read(),
            salat_name=data['name'],
            salat_amount=data['amount']
        )
        db.add(food)
        db.commit()

        await state.finish()
        await message.answer('Tabriklaymiz maxsulot qo''shildi'
                             )


async def salat_info_ru(message: types.Message):
    db = Session()
    food_items = db.query(SalatRu).all()
    db.close()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for food_item in food_items:
        button_text = f"{food_item.salat_name}"
        keyboard.add(types.KeyboardButton(text=button_text))
    delete_button = types.KeyboardButton(text="⬅Назад")
    keyboard.add(delete_button)

    await bot.send_message(chat_id=message.chat.id, text="Доступные салаты:", reply_markup=keyboard)


@dp.message_handler(
    lambda message: any(food_item.salat_name in message.text for food_item in Session().query(SalatRu).all()))
async def show_food_details(message: types.Message):
    db = Session()
    selected_food_name = next(
        (food_item.salat_name for food_item in db.query(SalatRu).all() if
         food_item.salat_name in message.text), None)
    if selected_food_name:
        try:

            selected_food_item = db.query(SalatRu).filter(SalatRu.salat_name == selected_food_name).first()

            photo = selected_food_item.salat_picture
            details_text = f" Номер салата : {selected_food_item.id}\nНазвание салата: {selected_food_item.salat_name}\nЦена салата : {selected_food_item.salat_amount}"
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=details_text,
                                 reply_markup=Salat_delete_ru()
                                 )
        finally:
            db.close()


@dp.message_handler(lambda message: message.text == "Посмотреть салаты")
async def start_food_registration(message: types.Message):
    await salat_info_ru(message)


@dp.callback_query_handler(lambda query: query.data == 'yдалить🥗', state="*")
async def process_delete(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    salat_name = get_selected_salat_name_ru()
    async with state.proxy() as data:
        data['salat_name'] = salat_name

        if salat_name:
            db = Session()
            food_item = db.query(SalatRu).filter_by(salat_name=salat_name).first()
            if food_item:
                food_item.salat_name = salat_name
                db.delete(food_item)
                db.commit()
            db.close()
            chat_id = query.message.chat.id

            await bot.send_message(chat_id=chat_id, text='✅ Данные удалены')

            data.clear()
            message_id = query.message.message_id

            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        else:

            await bot.answer_callback_query(query.id, text='❌ Информация не найдена')


@dp.callback_query_handler(lambda query: query.data == 'изменять🥗', state='*')
async def process_order(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    selected_food_name = get_selected_salat_name_ru()

    async with state.proxy() as data:
        data['salat_name'] = selected_food_name

    await Calat_ru.salat_amount.set()
    await query.message.answer("Пожалуйста, введите пересмотренную цену")


@dp.message_handler(state=Calat_ru.salat_amount)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['salat_amount'] = message.text
        ordered_food_name = data['salat_name']
        product = session.query(SalatRu).filter_by(salat_name=ordered_food_name).first()

        if product:

            product.salat_amount = data['salat_amount']

            session.commit()

            await message.answer('Измененная информация')

        else:
            await message.answer('Информация не изменилась')

    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'oтмена🥗')
async def delete_message(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    await bot.answer_callback_query(query.id, '✅ Удаление данных отменено ')
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


@dp.callback_query_handler(lambda query: query.data == 'oтмена🌊')
async def delete_message(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    await bot.answer_callback_query(query.id, '✅ Удаление данных отменено ')
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


@dp.callback_query_handler(lambda query: query.data == 'oтмена')
async def delete_message(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    await bot.answer_callback_query(query.id, '✅ Удаление данных отменено ')
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


@dp.message_handler(lambda message: message.text == "⏮Назад")
async def start_food_registration(message: types.Message):
    await message.answer('hello bro', reply_markup=admin_ru())


@dp.message_handler(lambda message: message.text == "⬅Назад")
async def start_food_registration(message: types.Message):
    await message.answer('Menu:', reply_markup=salat_ru())


'''--------------------------------------------------------------------------'''


@dp.callback_query_handler(lambda query: query.data == 'bekor')
async def delete_message(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    await bot.answer_callback_query(query.id, '✅ Malumotlarni o''chirish bekor qilindi ')
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


@dp.callback_query_handler(lambda query: query.data == 'bekor🌊')
async def delete_message(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    await bot.answer_callback_query(query.id, '✅ Malumotlarni o''chirish bekor qilindi ')
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


@dp.callback_query_handler(lambda query: query.data == 'bekor🥗')
async def delete_message(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    await bot.answer_callback_query(query.id, '✅ Malumotlarni o''chirish bekor qilindi ')
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


@dp.message_handler(lambda message: message.text == "⏮Orqaga")
async def start_food_registration(message: types.Message):
    await message.answer('hello bro', reply_markup=admin())


@dp.message_handler(lambda message: message.text == "⬅Orqaga")
async def start_food_registration(message: types.Message):
    await message.answer('Menu:', reply_markup=salat())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
