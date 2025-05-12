from sqlalchemy.ext.asyncio import AsyncSession

from src.core.users.models import UsersOrm
from src.core.users.schemas import SUser


class UsersRepository:
    def __init__(self, session):
        self._session: AsyncSession = session

    def add(self, user_dto: SUser):
        user_orm = UsersOrm(**user_dto.model_dump())
        self._session.add(user_orm)

    async def get_by_id(self, id: int):  # Make this method async
        user_orm = await self._session.get(UsersOrm, id)  # Await the get call
        if user_orm:
            user_dto = SUser.model_validate(user_orm)
            return user_dto
        return None

    async def delete(self, id: int):
        user_orm = await self._session.get(UsersOrm, id)
        if user_orm:
            await self._session.delete(user_orm)
        return None
