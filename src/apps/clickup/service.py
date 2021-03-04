import httpx

from . import serializer
from src.core.config import settings
from src.schemas.clickup import ClickUpTasks

CLIENT = httpx.AsyncClient()


class BaseClass:
    headers: dict = None

    def __init__(self, auth_token: str):
        self.headers = {"Authorization": auth_token}


class Users(BaseClass):

    async def get_user(self) -> dict:
        """Получение пользовательских данных"""
        url = 'https://api.clickup.com/api/v2/user'  # Получение данных о пользователе по токену.
        response = await CLIENT.get(url=url, headers=self.headers)
        assert response.status_code == 200

        return response.json()['user']

    @staticmethod
    async def get_auth_token(code: str) -> str:
        url = f'https://api.clickup.com/api/v2/oauth/token?' \
              f'client_id={settings.CLICKUP_CLIENT_ID}&' \
              f'client_secret={settings.CLICKUP_SECRET_KEY}&' \
              f'code={code}'

        response = await CLIENT.post(url=url)
        print(response)
        assert response.status_code == 200

        return response.json()['access_token']

    @staticmethod
    def get_verify_code_url():
        return f"https://app.clickup.com/api" \
               f"?client_id={settings.CLICKUP_CLIENT_ID}" \
               f"&redirect_uri=https://google.com"


class Teams(BaseClass):

    async def get_teams(self) -> list:
        url = 'https://api.clickup.com/api/v2/team'  # Получение данных о пользователе по токену.

        response = await CLIENT.get(url=url, headers=self.headers)
        assert response.status_code == 200

        return response.json()['teams']


class Tasks(BaseClass):

    async def get_tasks(self, team_id: int, click_user_id: int):
        url = f"https://api.clickup.com/api/v2/team/{team_id}/task?assignees%5B%5D={click_user_id}"

        response = await CLIENT.get(url=url, headers=self.headers)
        assert response.status_code == 200

        return response.json()['tasks']


class ClickUp(Users, Teams, Tasks):

    async def collect_user_tasks(self, click_user_id: int) -> ClickUpTasks:
        """
        Метод по сбору назначенных задач на пользователя по всему WorkSpace.

        Данный метод определяет тот WorkSpace который был выбран при подключении ClickUp и собирает по нему данные.
        Данные собираются по всем областям перебирая каждую сущность: Spaces, Folders, Folders List, Tasks.
        Перебор происходит из-за архитектуры clickup которая деклалирует сбор данных по этапно.
        Чтобы добраться до Tasks необходимо произвести всю цепочку.
        WorkSpace -> Spaces (list) -> Folders (list) -> FoldersLists (lists) -> Tasks (lists)
        """
        teams = await self.get_teams()

        prepared_tasks = []
        for team in teams:
            tasks = await self.get_tasks(team['id'], click_user_id)
            prepared_tasks += [serializer.prepare_task(x) for x in tasks if x['folder']['name'] != "Backlog"]

        return ClickUpTasks(tasks=prepared_tasks)
