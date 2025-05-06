from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot_api.keyboards.reply_kb import admin_kb
from src.core.users.schemas import SUser
from src.core.collecting_money.schemas import SCollection,SCollectionStatus, StatusEnum
from src.core.collecting_money.service import CollectionService

router = Router()

collection1 = {
    "id": 1,
    "target": "Project A",
    "description": "Description for Project A",
    "amount": 100,
    "is_active": True,
    "statuses": [
        {"user_id": 1, "collection_id": 1, "state": StatusEnum.UNSEEN},
        {"user_id": 2, "collection_id": 1, "state": StatusEnum.ACCEPT}
    ]
}

collection2 = {
    "id": 2,
    "target": "Project B",
    "description": "Description for Project B",
    "amount": 200,
    "is_active": True,
    "statuses": [
        {"user_id": 3, "collection_id": 2, "state": StatusEnum.TRANSFERRED}
    ]
}

collection3 = {
    "id": 3,
    "target": "Project C",
    "description": "Description for Project C",
    "amount": 150,
    "is_active": False,
    "statuses": [
        {"user_id": 4, "collection_id": 3, "state": StatusEnum.CONFIRMED}
    ]
}

collection4 = {
    "id": 4,
    "target": "Project D",
    "description": "Description for Project D",
    "amount": 300,
    "is_active": True,
    "statuses": [
        {"user_id": 5, "collection_id": 4, "state": StatusEnum.UNSEEN},
        {"user_id": 6, "collection_id": 4, "state": StatusEnum.ACCEPT}
    ]
}

collection5 = {
    "id": 5,
    "target": "Project E",
    "description": "Description for Project E",
    "amount": 250,
    "is_active": True,
    "statuses": [
        {"user_id": 7, "collection_id": 5, "state": StatusEnum.TRANSFERRED},
        {"user_id": 8, "collection_id": 5, "state": StatusEnum.UNSEEN}
    ]
}

# Список коллекций
list_collections = [collection1, collection2, collection3, collection4, collection5]
fake_collections = [SCollection.model_validate(collection) for collection in list_collections]

@router.message(Command(commands=["admin"]))
async def admin_cmd(message: types.Message):
    await message.reply(text="Будем командовать=)", reply_markup=admin_kb)

@router.message(Command(commands=["Создать сбор"]))
async def create_collection(message: types.Message):
    pass

@router.message(Command(commands=["Подтвердить"]))
async def select_collection(message: types.Message):
    change_collection = InlineKeyboardBuilder()
    #collections = CollectionService.get_active_collections()
    collections = fake_collections
    for collection in collections:
        change_collection.button(text=collection.target, callback_data=f'{collection.id}')
    await message.answer(text="Выберите сбор:", reply_markup=change_collection.adjust(1).as_markup())

@router.callback_query()
async def confirm_transfer(callback_query: types.CallbackQuery):
    collection_id = callback_query.data


