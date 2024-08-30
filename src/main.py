import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv, find_dotenv

from handlers.schedule import schedule_router

load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(schedule_router)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.reply('Hello, world!')




async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
