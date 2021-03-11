
from src.submodules.common.base_class import APIClass
from src.submodules.oauth.service import OAuth, OAuthUtils
from .schemas import ClickUpTasks, ClickUpCreateTask
from .serializer import prepare_task
from .settings import click_up_settings


class Users(APIClass):

    async def get_user_by_token(self) -> dict:
        """Получение пользовательских данных"""
        url = 'https://api.clickup.com/api/v2/user'  # Получение данных о пользователе по токену.

        r_json = await self.make_request("GET", url)
        return r_json['user']

    async def get_user_by_team_id_and_user_id(self, team_id: int, user_id: int) -> dict:
        """
        Получение пользовательских данных.

        Только для команд с Enterprise статусом. Без него будет возвращаться 403.
        """
        url = f'https://api.clickup.com/api/v2/team/{team_id}/user/{user_id}'

        r_json = await self.make_request("GET", url)
        return r_json['member']['user']

    async def get_users_by_task(self, task_id: str) -> dict:
        """Получение пользовательских данных"""
        url = f'https://api.clickup.com/api/v2/task/{task_id}/member'

        r_json = await self.make_request("GET", url)
        return r_json['members']


class Teams(APIClass):

    async def get_teams(self) -> list:
        url = 'https://api.clickup.com/api/v2/team'  # Получение данных о пользователе по токену.

        r_json = await self.make_request("GET", url)
        return r_json['teams']


class Spaces(APIClass):

    async def get_spaces(self, team_id: int) -> list:
        url = f"https://api.clickup.com/api/v2/team/{team_id}/space?archived=false"
        r_json = await self.make_request("GET", url)
        return r_json['spaces']


class Folders(APIClass):

    async def get_folders(self, space_id: int) -> list:
        url = f"https://api.clickup.com/api/v2/space/{space_id}/folder?archived=false"
        r_json = await self.make_request("GET", url)
        return r_json['folders']

    async def get_folder(self, folder_id: int) -> list:
        url = f"https://api.clickup.com/api/v2/folder/{folder_id}"
        r_json = await self.make_request("GET", url)
        return r_json


class Lists(APIClass):

    async def get_lists(self, folder_id: int):
        url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list?archived=false"
        r_json = await self.make_request("GET", url)
        return r_json['lists']


class Tasks(APIClass):

    async def get_tasks(self, team_id: int, click_user_id: int):
        url = f"https://api.clickup.com/api/v2/team/{team_id}/task?assignees%5B%5D={click_user_id}"

        r_json = await self.make_request("GET", url)
        return r_json['tasks']

    async def create_task(self, list_id: int, task: ClickUpCreateTask):
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task/"
        r_json = await self.make_request("POST", url, task.dict())
        return r_json

    async def get_task(self, task_id: str):
        url = f"https://api.clickup.com/api/v2/task/{task_id}/"

        r_json = await self.make_request("GET", url)
        return r_json


class ClickUp(Users, Teams, Spaces, Folders, Lists, Tasks):
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
            prepared_tasks += [
                prepare_task(x) for x in tasks if x['folder']['name'] != "Backlog" and x['list']['name'] != "Backlog"
            ]

        return ClickUpTasks(tasks=prepared_tasks)

    async def start_webhook_accepting(self, team_id: int, webhook_endpoint: str):
        """Метод для запуска получения уведомлений по разным событиям в кликап связанных с пользователем."""
        url = f"https://api.clickup.com/api/v2/team/{team_id}/webhook"

        # Endpoint - куда кликап будет отправлять запросы.
        # Events - список всех событий в clickup.
        payload = dict(endpoint=webhook_endpoint, events=["*"])

        r_json = await self.make_request("POST", url, payload)
        return r_json


class ClickUpOAuth(OAuth):
    """Класс с полным процессом получения авторизационного токена для работы с ClickUp."""

    client_id = click_up_settings.CLICKUP_CLIENT_ID
    client_secret = click_up_settings.CLICKUP_SECRET_KEY

    @staticmethod
    def get_code_url(redirect_uri: str, state: dict) -> str:
        """Шаг №1 Получение ссылки с кодом подтверждения."""
        return f"https://app.clickup.com/api" \
               f"?client_id={click_up_settings.CLICKUP_CLIENT_ID}" \
               f"&state={OAuthUtils.encode_state_to_base64(state)}" \
               f"&redirect_uri={redirect_uri}"

    @classmethod
    def get_token_url(cls, code: str, redirect_uri: str = None):
        return f'https://api.clickup.com/api/v2/oauth/token?' \
              f'client_id={click_up_settings.CLICKUP_CLIENT_ID}&' \
              f'client_secret={click_up_settings.CLICKUP_SECRET_KEY}&' \
              f'code={code}'
