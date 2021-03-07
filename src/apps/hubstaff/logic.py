import logging
from datetime import datetime

import httpx

from src.apps.users.logic import bind_data
from src.apps.users.schemas import UserData
from src.bot.commands.dispatcher import bot
from src.core.enums import WebhookUrlsEnum
from src.submodules.hubstaff.schemas import HubStaffActivityReports
from src.submodules.hubstaff.serializer import prepare_user_data
from src.submodules.hubstaff.service import HubStaff, HubStaffOAuth
from src.utils import get_webhook_url


async def add_hub_staff_data_by_user(user_id: int, code: str) -> None:
    """Добавление данных из HubStaff пользователю."""
    redirect_uri = get_webhook_url(WebhookUrlsEnum.oauth.value, short_url=False)
    token_data = await HubStaffOAuth().get_token(code, redirect_uri, is_basic_token=True)

    access_token = f"Bearer {token_data['access_token']}"
    hub_staff_user_data = await HubStaff(access_token).get_user()

    await bind_data(user_id, prepare_user_data(hub_staff_user_data, token_data))


async def refresh_token(user_data: UserData) -> None:
    """
    Обновление токена авторизации.

    Необходимо в случае если истек прошлый токен.
    """
    try:
        token_data = await HubStaffOAuth().get_refresh_token(user_data.hub_staff.refresh_token)
    except httpx.HTTPStatusError as exc:
        logging.error(f"{str(exc)}, {exc.response.text}")

        if exc.response.status_code == 400:
            await bot.send_message(user_data.user_id, "При обновлении токена произошла ошибка. Попробуйте позже.")
            return

        raise exc

    access_token = f"Bearer {token_data['access_token']}"
    hub_staff_user_data = await HubStaff(access_token).get_user()

    await bind_data(user_data.user_id, prepare_user_data(hub_staff_user_data, token_data))


async def get_activities_by_period(
        user_data: UserData,
        start_date: datetime,
        end_date: datetime
) -> HubStaffActivityReports:
    """Получение списка активностей за период вермени."""
    try:
        return await HubStaff(user_data.hub_staff.auth_token).collect_user_activities_by_period(start_date, end_date)
    except httpx.HTTPStatusError as exc:
        logging.error(f"{str(exc)}, {exc.response}")

        if exc.response.status_code == 401:

            logging.debug(f"Refreshing token by user:{user_data.user_id}")
            await bot.send_message(user_data.user_id, "Упс... Вероятно ваш токен истек, попробую получить новый....")
            await refresh_token(user_data)

        raise exc
