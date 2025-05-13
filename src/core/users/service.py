from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.users.models import UsersOrm
from src.core.users.schemas import SUser
from src.core.common.uow import uow

users_list = []

class UserIsExist(Exception):
    pass

class UserIsNotExist(Exception):
    pass

class UsersService:
    @staticmethod
    async def create_user(user_dto: SUser):
        async with uow:
            if await uow.users.get_by_id(user_dto.id):
                raise UserIsExist
            uow.users.add(user_dto)

    @staticmethod
    async def get_by_id(user_id: int):
        async with uow:
            user_dto = await uow.users.get_by_id(user_id)  # Await the call here
            if user_dto:
                return user_dto
            return None


    @staticmethod
    async def delete_user(user_id: int):
        async with uow:
            user = await uow.users.get_by_id(user_id)
            if user:
                await uow.users.delete(user_id)
            else:
                raise UserIsNotExist("Пользователь не существует.")