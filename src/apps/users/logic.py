from src.apps.users.crud import add_user, get_user
from src.apps.clickup.logic import Users

from pydantic import validate_arguments


@validate_arguments
async def add_new_user(user_id: int, auth_code: str):
    """Добавление нового пользователя в систему."""
    auth_token = await Users.get_auth_token(auth_code)

    user_data = dict(
        user_id=user_id,
        auth_token=auth_token['access_token']
    )
    user = await add_user(user_data)
    return user


async def get_user_by_telegram_id(user_id: int):
    """Получение пользователя по telegram-id"""
    user_data = await get_user(user_id)
    return user_data if user_data else None
