import base64
from datetime import datetime
from uuid import uuid4

from src.submodules.common.base_class import BaseClass, APIClass
from .schemas import HubStaffActivityReports, HubStaffTotalActivity
from .serializer import prepare_activity, prepare_task
from .settings import hub_staff_settings


class Users(APIClass):

    async def get_user(self) -> dict:
        """Получение пользовательских данных"""
        url = 'https://api.hubstaff.com/v2/users/me'  # Получение данных о пользователе по токену.

        r_json = await self._rs_get(url)
        return r_json['user']


class Organizations(APIClass):

    async def get_organizations(self) -> dict:
        """Получение пользовательских данных"""
        url = "https://api.hubstaff.com/v2/organizations"

        r_json = await self._rs_get(url)
        return r_json['organizations']


class Activities(APIClass):

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

        r_json = await self._rs_get(url)
        return r_json['daily_activities']


class Tasks(APIClass):

    async def get_task(self, task_id: int):
        url = f"https://api.hubstaff.com/v2/tasks/{task_id}"

        r_json = await self._rs_get(url)
        return r_json['task']


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


class HubStaffOAuth(BaseClass):
    """Класс с полным процессом получения авторизационного токена для работы с HubStaff."""

    @staticmethod
    def get_verify_code_url(redirect_uri: str, state: str) -> str:
        """Шаг №1 Получение ссылки с кодом подтверждения."""
        return f"https://account.hubstaff.com/authorizations/new" \
               f"?client_id={hub_staff_settings.HUBSTAFF_CLIENT_ID}" \
               f"&response_type=code" \
               f"&nonce={str(uuid4())}" \
               f"&state={state}" \
               f"&scope=openid hubstaff:read profile tasks:read" \
               f"&redirect_uri={redirect_uri}" \


    async def get_auth_token(self, verify_code: str, redirect_uri: str) -> dict:
        """Шаг №2 Получение токена авторизации с применением кода подтверждения."""
        url = "https://account.hubstaff.com/access_tokens" \
              "?grant_type=authorization_code" \
              f"&code={verify_code}" \
              f"&redirect_uri={redirect_uri}"

        headers = {"Authorization": f"Basic {self.get_basic_token_to_base64()}"}

        response = await self.client.post(url=url, headers=headers)
        assert response.status_code == 200

        return response.json()

    @staticmethod
    def get_basic_token_to_base64() -> str:
        """Шифрование Basic токена."""
        client_data_to_bytes = f'{hub_staff_settings.HUBSTAFF_CLIENT_ID}:{hub_staff_settings.HUBSTAFF_SECRET_KEY}'.encode()
        return base64.b64encode(client_data_to_bytes).decode()
