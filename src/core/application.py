import logging

from aiogram import executor

from src.db.database import users_db
from src.commands.dispatcher import dp

# Configure logging
logging.basicConfig(level=logging.INFO)

users_db.init_connection()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
