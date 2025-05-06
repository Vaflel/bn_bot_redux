import os
from io import BytesIO

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, BufferedInputFile

from src.core.schedule.service import ScheduleService
from src.core.users.service import UsersService
from src.config import settings

router = Router()

@router.message(Command(commands=["Расписание"]))
async def schedule_from_user(message: types.Message):
    user = await UsersService.get_by_id(message.from_user.id)
    if not user:
        await message.answer(text="Сначала зарегистрируйся")
    service = ScheduleService(user)
    image = service.create_schedule()

    # with open("img.png", "wb") as f:
    #     f.write(image)
    #file_path = f'../data/{user.group_name}_schedule.png'
    document = BufferedInputFile(image,filename=f"{user.name}_schedule")

    await message.answer_document(
        text=f"Расписание из байтов для {user.name}",
        document=document,
    )
    # print(1)
    # document2 = FSInputFile(path="img.png", filename="img")
    # await message.answer("Отправляю")
    # await message.answer_document(
    #     text="Расписание из файла",
    #     document=document2,
    # )
