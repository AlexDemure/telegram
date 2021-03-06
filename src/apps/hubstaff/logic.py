from datetime import datetime

from src.apps.users.logic import bind_hub_staff
from src.apps.users.schemas import UserData
from src.core.sessions import HTTP_CLIENT
from src.submodules.hubstaff.schemas import HubStaffUserData
from src.submodules.hubstaff.service import HubStaff, HubStaffOAuth
from src.core.config import settings


async def add_hub_staff_data_by_user(user_id: int, verify_code: str) -> None:
    """Добавление данных из HubStaff пользователю."""
    token_data = await HubStaffOAuth(HTTP_CLIENT).get_auth_token(verify_code, f"{settings.webhook_uri}/connect")
    hub_staff_user_data = await HubStaff(HTTP_CLIENT, f"Bearer {token_data['access_token']}").get_user()

    hub_staff_data = HubStaffUserData(
        id=hub_staff_user_data['id'],
        username=hub_staff_user_data['name'],
        email=hub_staff_user_data['email'],
        auth_token=f"Bearer {token_data['access_token']}",
        refresh_token=token_data['refresh_token']
    )
    await bind_hub_staff(user_id, hub_staff_data)


async def get_activities_by_period(user_data: UserData, start_date: datetime, end_date: datetime):
    """Получение списка активностей за период вермени."""
    reports = await HubStaff(
        HTTP_CLIENT, user_data.hub_staff.auth_token
    ).collect_user_activities_by_period(start_date, end_date)

    return reports
