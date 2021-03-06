import logging
from datetime import datetime
from typing import Optional, List

from pydantic import validate_arguments

from src.apps.users.crud import _add_user, _get_user, _get_users
from src.apps.users.crud import update_document
from src.apps.users.schemas import UserData, UserCreate
from src.apps.users.serializer import prepare_user_data
from src.submodules.clickup.schemas import ClickUpUserData
from src.submodules.hubstaff.schemas import HubStaffUserData


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


async def bind_click_up(user_id: int, click_up_data: ClickUpUserData):
    """Добавление к текущему пользователю данные от ClickUp."""
    user_data = await _get_user(user_id)
    if not user_data:
        await add_new_user(UserCreate(user_id=user_id, registration_at=datetime.utcnow()))
        user_data = await _get_user(user_id)

    user_data['click_up'] = click_up_data.dict()

    document_id = user_data.pop("_id")

    await update_document(document_id, user_data)
    logging.debug("Token is bind to user.")


async def bind_hub_staff(user_id: int, hub_staff_data: HubStaffUserData):
    """Добавление к текущему пользователю данные от HubStaff."""
    user_data = await _get_user(user_id)
    if not user_data:
        await add_new_user(UserCreate(user_id=user_id, registration_at=datetime.utcnow()))
        user_data = await _get_user(user_id)

    user_data['hub_staff'] = hub_staff_data.dict()

    document_id = user_data.pop("_id")

    await update_document(document_id, user_data)
    logging.debug("Token is bind to user.")
