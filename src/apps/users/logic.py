import logging
from datetime import datetime
from typing import Optional, List, Union

from pydantic import validate_arguments

from src.apps.users.crud import (
    _add_user, _get_user,  _get_click_up_owner,
    _get_users, _get_user_by_click_up_id, _get_any_user_with_click_up_access_token
)
from src.apps.users.crud import update_document
from src.apps.users.schemas import UserData, UserCreate
from src.apps.users.serializer import prepare_user_data
from src.submodules.clickup.schemas import ClickUpUserData
from src.submodules.hubstaff.schemas import HubStaffUserData
from src.bot.utils import get_user_by_chat_id


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


async def bind_data(user_id: int, data: Union[ClickUpUserData, HubStaffUserData]):
    """Обновление сервисных данных пользователю."""
    user_data = await _get_user(user_id)
    if not user_data:
        user = await get_user_by_chat_id(user_id)
        await add_new_user(UserCreate(user_id=user_id, username=user['username'], registration_at=datetime.utcnow()))
        user_data = await _get_user(user_id)

    if isinstance(data, ClickUpUserData):
        user_data['click_up'] = data.dict()
    elif isinstance(data, HubStaffUserData):
        user_data['hub_staff'] = data.dict()
    else:
        return

    document_id = user_data.pop("_id")

    await update_document(document_id, user_data)
    logging.debug("Data is bind to user.")


@validate_arguments
async def get_click_up_user(click_up_user_id: int, get_owner_if_null: bool = False) -> Optional[UserData]:
    """Получение пользователя по click_up_user_id"""
    user_data = await _get_user_by_click_up_id(click_up_user_id)
    if user_data:
        return prepare_user_data(user_data)
    else:
        if get_owner_if_null:
            user_data = await _get_click_up_owner()
            if user_data:
                return prepare_user_data(user_data)

        return None


async def get_any_click_up_user_with_access_token() -> Optional[UserData]:
    """Получение любого пользователя с токеном."""
    user_data = await _get_any_user_with_click_up_access_token()
    if user_data:
        return prepare_user_data(user_data)
    else:
        return None
