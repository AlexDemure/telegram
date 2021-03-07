from datetime import datetime

from src.apps.users.logic import bind_data
from src.apps.users.schemas import UserData
from src.utils import get_webhook_url
from src.submodules.hubstaff.serializer import prepare_user_data
from src.submodules.hubstaff.service import HubStaff, HubStaffOAuth
from src.submodules.oauth.settings import OAUTH_ENDPOINT


async def add_hub_staff_data_by_user(user_id: int, code: str) -> None:
    """Добавление данных из HubStaff пользователю."""
    redirect_uri = get_webhook_url(OAUTH_ENDPOINT, short_url=False)
    token_data = await HubStaffOAuth().get_auth_token(code, redirect_uri, is_basic_token=True)

    access_token = f"Bearer {token_data['access_token']}"
    hub_staff_user_data = await HubStaff(access_token).get_user()

    await bind_data(user_id, prepare_user_data(hub_staff_user_data, token_data))


async def get_activities_by_period(user_data: UserData, start_date: datetime, end_date: datetime):
    """Получение списка активностей за период вермени."""
    return await HubStaff(user_data.hub_staff.auth_token).collect_user_activities_by_period(start_date, end_date)
