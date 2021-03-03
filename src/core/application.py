from aiogram import executor

from src.db.database import users_db
from src.commands.dispatcher import dp
from src.core import scheduler

users_db.init_connection()

scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
