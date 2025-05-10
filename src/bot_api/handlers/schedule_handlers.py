from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile

from src.core.schedule.service import ScheduleService
from src.core.users.service import UsersService

router = Router()

@router.message(Command(commands=["Расписание"]))
async def schedule_from_user(message: types.Message):
    user = await UsersService.get_by_id(message.from_user.id)
    if not user:
        await message.answer(text="Сначала зарегистрируйся")
    service = ScheduleService(user)
    image = service.create_schedule()
    document = BufferedInputFile(image,filename=f"{user.name}_schedule.png")
    await message.answer_document(
        text=f"Расписание из байтов для {user.name}",
        document=document,
    )
