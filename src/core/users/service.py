from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.users.models import UsersOrm
from src.core.users.schemas import SUser
from src.core.common.uow import uow

users_list = []

class UserIsExist(Exception):
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



# class UsersService:
#     @staticmethod
#     async def get_by_id(
#             user_id: int,
#             session: Session = new_session
#     ) -> SUser:
#         stmt = select(UsersOrm).where(UsersOrm.id == user_id)
#         result = await session.execute(stmt)
#         return SUser.model_validate(result.scalar())
#
#     @staticmethod
#     async def get_list(session: Session = new_session) -> list[SUser]:
#         stmt = select(UsersOrm)
#         result = await session.execute(stmt)
#         users = result.scalars().all()
#         return [SUser.model_validate(user) for user in users]
#
#     @staticmethod
#     async def get_list_by_groupname(
#             group_name: str,
#             session: Session = new_session,
#     ) -> list[SUser]:
#         stmt = (
#             select(UsersOrm)
#             .where(UsersOrm.group_name==group_name)
#         )
#         result = await session.execute(stmt)
#         users = result.scalars().all()
#         return [SUser.model_validate(user) for user in users]
#
#     @staticmethod
#     async def create_user(
#             user_dto: SUser,
#             session: Session = new_session
#     ):
#         user = UsersOrm(**user_dto.model_dump())
#         session.add(user)
#         session.commit()