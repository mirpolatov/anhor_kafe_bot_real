from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from button.admin_button import main_rp, food_delete, food

from db import Session, MainMenu, Menu
from funksiyalar.funksiya1 import get_selected_food_name, get_selected_food_name2

from state.state_uz import Forms, Form

Token = '6786217148:AAEFeJlJsySajQVreFmSHw5vRdNiZNP_7FI'

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

session = Session()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id != 5161994540 and message.from_user.id != 1930798399 and message.from_user.id != 5772722670:
        await message.answer('Salom')
    else:
        await message.answer("Salom admin", reply_markup=main_rp())


'''-----------------------UZ------------------------'''
'''----------------------------Ovqatlar-----------------------------------'''


@dp.message_handler(lambda message: message.text == "Maxsulot qo'shish")
async def start_food_registration(message: types.Message):
    await message.answer("Iltimos,maxsulot rasmini kiriting.")
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
    await message.answer("Iltimos,maxsulot nomini kiriting:", reply_markup=food())


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
        food = MainMenu(
            food_picture=downloaded_file.read(),
            name=data['food_name'],
            price=data['amount'],
        )

        db.add(food)
        db.commit()
        foods = Menu(
            name=data['food_name'],
            callback_data=data['food_name'],
            price=data['amount'],
            food_id=food.id
        )
        db.add(foods)
        db.commit()

        await state.finish()
        await message.answer(
            'Tabriklaymiz maxsulot qo''shildi'
        )


async def food_info(message: types.Message):
    db = Session()
    food_items = db.query(MainMenu).all()
    db.close()

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)

    for food_item in food_items:
        button_text = f"{food_item.name}"
        keyboard.add(types.KeyboardButton(text=button_text))

    delete_button = types.KeyboardButton(text="🔙Orqaga")
    keyboard.add(delete_button)

    await bot.send_message(chat_id=message.chat.id, text="Mavjud maxsulotlar:", reply_markup=keyboard)


@dp.message_handler(
    lambda message: any(food_item.name in message.text for food_item in Session().query(MainMenu).all()))
async def show_food_details(message: types.Message):
    db = Session()
    selected_name = next(
        (food_item.name for food_item in db.query(MainMenu).all() if food_item.name in message.text), None)
    if selected_name:
        try:

            selected_food_item = db.query(MainMenu).filter(MainMenu.name == selected_name).first()
            selected_food_item2 = db.query(Menu).filter(Menu.name == selected_name).first()
            photo = selected_food_item.food_picture
            details_text = f" \nMaxsulot nomi: {selected_food_item.name}\nMaxsulot summasi: {selected_food_item2.price}"
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=details_text,
                                 reply_markup=food_delete())
        finally:
            db.close()


@dp.message_handler(lambda message: message.text == "Maxsulot ko'rish")
async def start_food_registration(message: types.Message):
    await food_info(message)


@dp.message_handler(lambda message: message.text == "✖")
async def start_food_registration(message: types.Message):
    await message.answer('hello word', reply_markup=main_rp())


from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda query: query.data == 'delete', state="*")
async def process_delete(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    selected_food_name = get_selected_food_name()
    selected_food_name2 = get_selected_food_name2()

    async with state.proxy() as data:
        data['food_name'] = selected_food_name and selected_food_name2

        if selected_food_name and selected_food_name2:
            db = Session()
            food_item = db.query(MainMenu).filter_by(name=selected_food_name).first()
            food_item2 = db.query(Menu).filter_by(name=selected_food_name2).first()

            if food_item and food_item2:
                db.delete(food_item)
                db.delete(food_item2)
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
    selected_food_name2 = get_selected_food_name2()

    async with state.proxy() as data:
        data['food_name'] = selected_food_name and selected_food_name2

    await Form.amount.set()
    await query.message.answer("Iltimos o'zgartirilgan narxni kiriting")


@dp.message_handler(state=Form.amount)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
        ordered_food_name = data['food_name']
        product = session.query(MainMenu).filter_by(name=ordered_food_name).first()
        product2 = session.query(Menu).filter_by(name=ordered_food_name).first()

        if product and product2:
            try:
                product.price = data['amount']
                product2.price = data['amount']
                session.commit()
                await message.answer('O\'zgardi')
            except Exception as e:
                session.rollback()  # Rollback changes if an exception occurs
                await message.answer(f'Xatolik: {str(e)}')
        else:
            await message.answer('O\'zgarmadi')

    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'bekor')
async def delete_message(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    await bot.answer_callback_query(query.id, '✅ Malumotlarni o''chirish bekor qilindi ')
    await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


@dp.message_handler(lambda message: message.text == "🔙Orqaga")
async def start_food_registration(message: types.Message):
    await message.answer('Menu :', reply_markup=main_rp())


@dp.message_handler(lambda message: message.text == "✖")
async def start_food_registration(message: types.Message):
    await message.answer('hello word', reply_markup=main_rp())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
