import base64
from datetime import datetime
from uuid import uuid4

import httpx

from src.apps.hubstaff.serializer import prepare_activity, prepare_task
from src.core.config import settings
from src.schemas.hubstaff import HubStaffActivityReports, HubStaffTotalActivity

CLIENT = httpx.AsyncClient()


class BaseClass:

    headers: dict = None

    def __init__(self, auth_token: str):
        self.headers = {"Authorization": auth_token}


class Users(BaseClass):

    async def get_user(self) -> dict:
        """Получение пользовательских данных"""
        url = 'https://api.hubstaff.com/v2/users/me'  # Получение данных о пользователе по токену.

        response = await CLIENT.get(url=url, headers=self.headers)
        print(response)
        assert response.status_code == 200

        return response.json()['user']

    @classmethod
    async def get_auth_token(cls, code: str) -> dict:
        url = "https://account.hubstaff.com/access_tokens" \
              "?grant_type=authorization_code" \
              f"&code={code}" \
              "&redirect_uri=https://google.com"

        headers = {"Authorization": f"Basic {cls.encode_data_to_base64()}"}

        response = await CLIENT.post(url=url, headers=headers)
        assert response.status_code == 200

        return response.json()

    @staticmethod
    def encode_data_to_base64() -> str:
        client_data_to_bytes = f'{settings.HUBSTAFF_CLIENT_ID}:{settings.HUBSTAFF_SECRET_KEY}'.encode()
        return base64.b64encode(client_data_to_bytes).decode()

    @staticmethod
    def get_verify_code_url():
        return f"https://account.hubstaff.com/authorizations/new" \
               f"?client_id={settings.HUBSTAFF_CLIENT_ID}" \
               f"&response_type=code" \
               f"&nonce={str(uuid4())}" \
               f"&redirect_uri=https://google.com" \
               f"&scope=openid hubstaff:read profile tasks:read"


class Organizations(BaseClass):

    async def get_organizations(self) -> dict:
        """Получение пользовательских данных"""
        url = "https://api.hubstaff.com/v2/organizations"

        response = await CLIENT.get(url=url, headers=self.headers)
        assert response.status_code == 200

        return response.json()['organizations']


class Activities(BaseClass):

    async def get_daily_activities(
            self,
            organization_id: int,
            hub_staff_user_id: int,
            start_date: datetime,
            end_date: datetime
    ) -> list:
        """Получение данных по активности пользователя."""
        url = f"https://api.hubstaff.com/v2/organizations/{organization_id}/activities/daily" \
               f"?date[start]={start_date.date().strftime('%Y-%m-%d')}" \
               f"&date[stop]={end_date.date().strftime('%Y-%m-%d')}" \
               f"&user_ids={hub_staff_user_id}'"

        response = await CLIENT.get(url=url, headers=self.headers)
        assert response.status_code == 200

        return response.json()['daily_activities']


class Tasks(BaseClass):

    async def get_task(self, task_id: int):
        url = f"https://api.hubstaff.com/v2/tasks/{task_id}"

        response = await CLIENT.get(url=url, headers=self.headers)
        assert response.status_code == 200

        return response.json()['task']


class HubStaff(Users, Organizations, Activities, Tasks):

    async def collect_user_activities_by_period(
            self, start_date: datetime, end_date: datetime
    ) -> HubStaffActivityReports:
        """Сбор всех активностей пользователя по опрд. периоду времени."""
        reports = list()

        hub_staff_user = await self.get_user()

        organizations = await self.get_organizations()
        for organization in organizations:
            activities = await self.get_daily_activities(
                organization_id=organization['id'],
                hub_staff_user_id=hub_staff_user['id'],
                start_date=start_date,
                end_date=end_date
            )

            total_tracked = sum([x['tracked'] for x in activities])
            total_activity = sum([x['overall'] for x in activities])

            prepared_activities = list()

            for activity in activities:
                try:
                    task = prepare_task(await self.get_task(activity['task_id']))
                except AssertionError as e:
                    print(str(e), activity)
                    continue

                prepared_activity = prepare_activity(activity, task)

                prepared_activities.append(prepared_activity)

            reports.append(
                HubStaffTotalActivity(
                    organization_id=organization['id'],
                    organization_name=organization['name'],
                    activities=prepared_activities,
                    total_activity=total_activity,
                    total_tracked=total_tracked,
                )
            )

        return HubStaffActivityReports(reports=reports)
