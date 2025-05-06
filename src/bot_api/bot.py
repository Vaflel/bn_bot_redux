from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from config import settings

from src.bot_api.handlers.schedule_handlers import router as schedule_router
# from src.bot_api.handlers.collection_handlers import router as collections_router
from src.bot_api.handlers.login_handlers import router as login_router
from src.bot_api.keyboards.reply_kb import main_kb

from src.core.users.schemas import SUser
from src.core.users.service import UsersService

bot = Bot(
    token=settings.TOKEN,
    timeout=180,
)
dp = Dispatcher()
dp.include_router(schedule_router)
# dp.include_router(collections_router)
dp.include_router(login_router)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    test_user = SUser(
        id=836309692,
        name="Климанова П.",
        group_name="МД-21-о",
        department_name="Факультет искусств и физической культуры",
    )
    await UsersService.create_user(test_user)
    await message.reply(text='Привет, чем могу помочь?', reply_markup=main_kb)
