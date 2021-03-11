# import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.core.config import settings

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Configure logging
# logging.basicConfig(level=logging.DEBUG)

# dp.middleware.setup(LoggingMiddleware())

from src.bot.commands.clickup import tasks
from src.bot.commands.hubstaff import activities
from src.bot.commands.users import oauth, services
from src.bot.commands import start
from src.bot.callbacks.clickup import tasks