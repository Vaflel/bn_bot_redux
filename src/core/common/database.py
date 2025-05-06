import os.path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings
from src.core.users.models import UsersOrm
from src.core.common.models import Model

db_path = os.path.join(settings.DATA_DIRECTORY, "bot.db")
engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}")
new_session = async_sessionmaker(engine, expire_on_commit=False)




async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
        print("Таблицы созданы")



async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
