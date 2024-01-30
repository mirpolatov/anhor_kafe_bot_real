from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from keyboard_uz import language

Token = '6934071728:AAFRgllllnh2Oew0d9t8aAdHEUepAFWOOAg'

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Тилни танланг  /   Выберите язык", reply_markup=language)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text='Bizda bunday buyruq mavjud emas.   /    У нас нет такого приказа.', reply=message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
