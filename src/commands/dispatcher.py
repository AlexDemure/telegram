from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.core.config import settings

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

from . import start, tasks, users
