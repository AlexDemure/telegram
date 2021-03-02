import httpx

from typing import List
from . import schemas, serializer
from src.core.config import settings

CLIENT = httpx.AsyncClient()


class BaseClass:

    headers: dict = None

    def __init__(self, auth_token: str):
        self.headers = {"Authorization": auth_token}


class Users(BaseClass):

    get_user_url = 'https://api.clickup.com/api/v2/user'  # Получение данных о пользователе по токену.

    async def _get_user(self) -> dict:
        """Получение пользовательских данных"""
        response = await CLIENT.get(url=self.get_user_url, headers=self.headers)
        assert response.status_code == 200

        return response.json()

    @classmethod
    async def get_auth_token(cls, code: str) -> dict:
        response = await CLIENT.post(url=cls.get_auth_token_url(code))
        assert response.status_code == 200

        return response.json()

    @staticmethod
    def get_auth_token_url(code: str):
        return f'https://api.clickup.com/api/v2/oauth/token?' \
               f'client_id={settings.CLICKUP_CLIENT_ID}&' \
               f'client_secret={settings.CLICKUP_SECRET_KEY}&' \
               f'code={code}'


class Teams(BaseClass):

    get_teams_url = 'https://api.clickup.com/api/v2/team'  # Получение данных о пользователе по токену.

    async def _get_teams(self) -> list:
        response = await CLIENT.get(url=self.get_teams_url, headers=self.headers)
        assert response.status_code == 200

        return response.json()['teams']


class Tasks(BaseClass):

    async def _get_tasks(self, team_id: int, user_id: int):
        response = await CLIENT.get(url=self._get_tasks_url(team_id, user_id), headers=self.headers)
        assert response.status_code == 200

        return response.json()['tasks']

    @staticmethod
    def _get_tasks_url(team_id: int, user_id: int):
        return f"https://api.clickup.com/api/v2/team/{team_id}/task?assignees%5B%5D={user_id}"


class ClickUp(Users, Teams, Tasks):

    user: schemas.UserData = None

    async def get_user(self) -> schemas.UserData:
        """Получение данных аккаунта пользователя."""
        self.user = serializer.prepare_user_data(await self._get_user())
        return self.user

    async def get_teams(self) -> List[schemas.TeamData]:
        """Получение списка workspace-ов у пользователя."""
        teams = await self._get_teams()
        return [serializer.prepare_team(x) for x in teams]

    async def get_tasks(self, team: schemas.TeamData) -> List[schemas.TaskItem]:
        """Получение списка задач по id-workspace."""
        tasks = await self._get_tasks(team.id, self.user.id)
        return [serializer.prepare_task(x) for x in tasks if x['folder']['name'] != "Backlog"]

    async def collect_user_tasks(self) -> schemas.UserTasks:
        """
        Метод по сбору назначенных задач на пользователя по всему WorkSpace.

        Данный метод определяет тот WorkSpace который был выбран при подключении ClickUp и собирает по нему данные.
        Данные собираются по всем областям перебирая каждую сущность: Spaces, Folders, Folders List, Tasks.
        Перебор происходит из-за архитектуры clickup которая деклалирует сбор данных по этапно.
        Чтобы добраться до Tasks необходимо произвести всю цепочку.
        WorkSpace -> Spaces (list) -> Folders (list) -> FoldersLists (lists) -> Tasks (lists)
        """
        user = await self.get_user()
        teams = await self.get_teams()

        prepared_tasks = []
        for team in teams:
            tasks = await self.get_tasks(team)
            prepared_tasks += tasks

        return schemas.UserTasks(tasks=prepared_tasks, user=user)

