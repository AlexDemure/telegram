from src.bot.dispatcher import bot


async def get_user_by_chat_id(chat_id: int) -> dict:
    chat = await bot.get_chat(chat_id)
    return chat.values

