from datetime import datetime
from uuid import uuid4

from src.submodules.common.base_class import APIClass
from src.submodules.oauth.service import OAuth, OAuthUtils
from .schemas import HubStaffActivityReports, HubStaffTotalActivity
from .serializer import prepare_activity, prepare_task
from .settings import hub_staff_settings


class Users(APIClass):

    async def get_user(self) -> dict:
        """Получение пользовательских данных"""
        url = 'https://api.hubstaff.com/v2/users/me'  # Получение данных о пользователе по токену.

        r_json = await self.make_request("GET", url)
        return r_json['user']


class Organizations(APIClass):

    async def get_organizations(self) -> dict:
        """Получение пользовательских данных"""
        url = "https://api.hubstaff.com/v2/organizations"

        r_json = await self.make_request("GET", url)
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

        r_json = await self.make_request("GET", url)
        return r_json['daily_activities']


class Tasks(APIClass):

    async def get_task(self, task_id: int):
        url = f"https://api.hubstaff.com/v2/tasks/{task_id}"

        r_json = await self.make_request("GET", url)
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


class HubStaffOAuth(OAuth):
    """Класс с полным процессом получения авторизационного токена для работы с HubStaff."""

    client_id = hub_staff_settings.HUBSTAFF_CLIENT_ID
    client_secret = hub_staff_settings.HUBSTAFF_SECRET_KEY

    @staticmethod
    def get_code_url(redirect_uri: str, state: dict) -> str:
        return f"https://account.hubstaff.com/authorizations/new" \
               f"?client_id={hub_staff_settings.HUBSTAFF_CLIENT_ID}" \
               f"&response_type=code" \
               f"&nonce={str(uuid4())}" \
               f"&state={OAuthUtils.encode_state_to_base64(state)}" \
               f"&scope=openid hubstaff:read profile tasks:read" \
               f"&redirect_uri={redirect_uri}" \


    @staticmethod
    def get_token_url(code: str, redirect_uri: str = None) -> str:
        return "https://account.hubstaff.com/access_tokens" \
               "?grant_type=authorization_code" \
               f"&code={code}" \
               f"&redirect_uri={redirect_uri}"

    @staticmethod
    def get_refresh_token_url(refresh_token: str) -> str:
        return "https://account.hubstaff.com/access_tokens" \
               "?grant_type=refresh_token" \
               f"&scope=openid hubstaff:read profile tasks:read" \
               f"&refresh_token={refresh_token}"

    async def get_refresh_token(self, refresh_token: str) -> dict:
        """Получение токена через Refresh Token."""
        access_basic_token = f"Basic {OAuthUtils.get_basic_token_to_base64(self.client_id, self.client_secret)}"
        self._headers['Authorization'] = access_basic_token

        url = self.get_refresh_token_url(refresh_token)
        return await self.make_request("POST", url)
