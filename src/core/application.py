from aiogram import executor

from src.bot.commands.dispatcher import dp
from src.core import scheduler
from src.db.database import users_db

users_db.init_connection()

scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
