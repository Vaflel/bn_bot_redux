from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types, F
from aiogram.filters import Command

from src.bot_api.utils.departments_list import departments_short_names
from src.core.users.service import UsersService, UserIsExist
from src.core.users.schemas import SUser
from src.bot_api.keyboards.login_kb import login_keyboard

router = Router()


class UserForm(StatesGroup):
    name = State()
    department_name = State()
    group_name = State()


@router.message(Command(commands=["отмена"]))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text="Отменено")


@router.message(Command(commands=["login"]))
async def login(message: types.Message, state: FSMContext) -> None:
    await state.set_state(UserForm.name)
    await message.answer(text="Введи своё имя в формате Иванов И.")


@router.message(UserForm.name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(UserForm.department_name)
    await message.answer(text=f"Хорошо, выбери свой факультет", reply_markup=login_keyboard)


@router.callback_query(UserForm.department_name)
async def process_department_name(callback: types.CallbackQuery, state: FSMContext):
    department_name = departments_short_names.get(callback.data)
    await state.update_data(department_name=department_name)
    await state.set_state(UserForm.group_name)
    await callback.message.answer(text=f"Хорошо, введи название своей группы")
    await callback.answer()


@router.message(UserForm.group_name)
async def process_group_name(message: types.Message, state: FSMContext):
    data = await state.update_data(group_name=message.text)
    user = SUser(
        id=message.from_user.id,
        name=data.get("name"),
        group_name=data.get("group_name"),
        department_name=data.get("department_name"),
    )
    try:
        await UsersService.create_user(user)
        text = f"Пользователь создан, теперь в расписание будут добавляться индивидуальные занятия для {user.name}"
        await message.answer(text=text)
    except UserIsExist:
        await message.answer("Пользователь уже существует")
    await state.clear()
