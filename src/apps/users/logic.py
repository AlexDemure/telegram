import logging
from typing import Optional, List

from pydantic import validate_arguments

from src.apps.users.crud import _add_user, _get_user, _get_users
from src.apps.users.crud import update_document
from src.apps.users.schemas import UserData, UserCreate
from src.apps.users.serializer import prepare_user_data


@validate_arguments
async def add_new_user(user_data: UserCreate) -> UserData:
    """Добавление нового пользователя в систему."""
    user = await _get_user(user_data.user_id)
    if not user:
        await _add_user(user_data.dict())
        user = await _get_user(user_data.user_id)
        logging.debug("User is created.")
    else:
        logging.debug("User already exists.")

    return prepare_user_data(user)


@validate_arguments
async def get_user(user_id: int) -> Optional[UserData]:
    """Получение пользователя по telegram-id"""
    user_data = await _get_user(user_id)
    if user_data:
        return prepare_user_data(user_data)
    else:
        return None


async def get_users() -> List[UserData]:
    users = await _get_users()
    return [prepare_user_data(x) for x in users]


async def bind_clickup_token(user_id, token: str):
    user_data = await _get_user(user_id)
    user_data['clickup_token'] = token

    document_id = user_data.pop("_id")

    await update_document(document_id, user_data)
    logging.debug("Token is bind to user.")


async def bind_hubstaff_token(user_id, token: str, refresh_token: str):
    user_data = await _get_user(user_id)
    user_data['hubstaff_token'] = token
    user_data['hubstaff_refresh_token'] = refresh_token

    document_id = user_data.pop("_id")

    await update_document(document_id, user_data)
    logging.debug("Token is bind to user.")
