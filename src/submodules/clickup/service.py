
from src.submodules.common.base_class import BaseClass, APIClass
from .schemas import ClickUpTasks
from .serializer import prepare_task
from .settings import click_up_settings


class Users(APIClass):

    async def get_user(self) -> dict:
        """Получение пользовательских данных"""
        url = 'https://api.clickup.com/api/v2/user'  # Получение данных о пользователе по токену.

        r_json = await self._rs_get(url)
        return r_json['user']


class Teams(APIClass):

    async def get_teams(self) -> list:
        url = 'https://api.clickup.com/api/v2/team'  # Получение данных о пользователе по токену.

        r_json = await self._rs_get(url)
        return r_json['teams']


class Tasks(APIClass):

    async def get_tasks(self, team_id: int, click_user_id: int):
        url = f"https://api.clickup.com/api/v2/team/{team_id}/task?assignees%5B%5D={click_user_id}"

        r_json = await self._rs_get(url)
        return r_json['tasks']


class ClickUp(Users, Teams, Tasks):
    """
    Класс для работы с ClickUP API.
    """

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
            prepared_tasks += [prepare_task(x) for x in tasks if x['folder']['name'] != "Backlog"]

        return ClickUpTasks(tasks=prepared_tasks)


class ClickUpOAuth(BaseClass):
    """Класс с полным процессом получения авторизационного токена для работы с ClickUp."""

    @staticmethod
    def get_verify_code_url() -> str:
        """Шаг №1 Получение ссылки с кодом подтверждения."""
        return f"https://app.clickup.com/api" \
               f"?client_id={click_up_settings.CLICKUP_CLIENT_ID}" \
               f"&redirect_uri=https://google.com"

    async def get_auth_token(self, verify_code: str) -> str:
        """Шаг №2 Получение токена авторизации с применением кода подтверждения."""

        url = f'https://api.clickup.com/api/v2/oauth/token?' \
              f'client_id={click_up_settings.CLICKUP_CLIENT_ID}&' \
              f'client_secret={click_up_settings.CLICKUP_SECRET_KEY}&' \
              f'code={verify_code}'

        response = await self.client.post(url=url)
        assert response.status_code == 200

        return response.json()['access_token']
