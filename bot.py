import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv
from handlers import  user_private, admin
from handlers.user_group import user_group_router


from database.engine import create_db, drop_db, async_sessionmaker
from middlewares.db import DataBaseSession

# Загружаем переменные окружения
load_dotenv()

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"))
bot.my_admins_list = []
dp = Dispatcher()

ALLOWED_UPDATES = ['message, edited_message']


# Регистрация обработчиков
dp.include_router(user_private.router)
dp.include_router(user_group_router)
dp.include_router(admin.admin_router)


async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()
    await create_db()

async def on_shutdown(bot):
    print("Бот лег")



# Запуск бота
async def main():
    await dp.start_polling(bot)

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=async_sessionmaker))
    await bot.delete_webhook(drop_pending_updates=True)


    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())