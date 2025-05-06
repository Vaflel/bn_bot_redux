import asyncio

from src.bot_api.bot import bot, dp
from src.core.common.database import create_tables, delete_tables



async def main():
    await delete_tables()
    await create_tables()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
