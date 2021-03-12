import logging
from typing import Optional

import httpx
from aiogram.types import ParseMode
from pydantic import validate_arguments

from src.apps.users.logic import bind_data, get_click_up_user, get_any_click_up_user_with_access_token
from src.apps.users.schemas import UserData
from src.bot.dispatcher import bot
from src.bot.messages.clickup.tasks import (
    prepare_response_notification_assignee, prepare_response_notification_comment_post
)
from src.core.enums import WebhookUrlsEnum
from src.submodules.clickup.enums import Priority, Tags, Teams, ClickUpAssigneeTypes, ClickUpTaskStatusType
from src.submodules.clickup.schemas import (
    ClickUpTasks, UserGroups, ClickUpUser, TeamData, ClickUpData, FolderData, ListData, SpaceData, ClickUpCreateTask,
    MemberItem
)
from src.submodules.clickup.serializer import prepare_user_data, prepare_task
from src.submodules.clickup.service import ClickUp, ClickUpOAuth
from src.utils import get_webhook_url


class ClickUpWebhookController:
    click_up: ClickUp = None

    webhook: dict = None
    access_token: str = None
    team_id: int = None

    async def init_connection(self, access_token: str = None, team_id: int = None) -> None:
        """
        Инициализация webhook для получения уведомлений из ClickUp.
        """
        if self.webhook is not None:
            logging.debug(f'Webhook is active:{self.webhook["id"]}')
            return

        if access_token is None:
            user_data = await get_any_click_up_user_with_access_token()
            if not user_data:
                logging.debug("ClickUp users in not found")
                return

            self.access_token = user_data.click_up.auth_token
        else:
            self.access_token = access_token

        self.click_up = ClickUp(self.access_token)

        if team_id is None:
            teams = await self.click_up.get_teams()
            if len(teams) > 0:
                self.team_id = teams[0]['id']
            else:
                raise ValueError("Teams is not found")
        else:
            self.team_id = team_id

        webhook_endpoint = get_webhook_url(
            WebhookUrlsEnum.click_up_webhook_notifications.value,
            short_url=False
        )

        await self.clear_webhooks()

        self.webhook = await self.click_up.create_webhook(team_id=self.team_id, endpoint=webhook_endpoint)
        logging.debug(f"Create webhook connection:{self.webhook['id']}")

    async def clear_webhooks(self) -> None:
        webhooks = await self.webhook_list()
        for webhook in webhooks:
            logging.debug(f"Delete webhook:{webhook['id']}")
            await self.click_up.delete_webhook(webhook['id'])

    async def webhook_list(self) -> list:
        if self.click_up is None:
            return []
        else:
            return await self.click_up.get_webhooks(team_id=self.team_id)


webhook_contoller = ClickUpWebhookController()


@validate_arguments
async def add_click_up_data_by_user(user_id: int, code: str) -> None:
    """Добавление данных из ClickUp пользователю."""
    token_data = await ClickUpOAuth().get_token(code)

    clickup = ClickUp(token_data['access_token'])

    user_data = await clickup.get_user_by_token()

    # Пытаемся получить Роль пользователя
    # т.к. получение пользователя из токена не показывает какая роль у него.
    user_role = None
    teams = await clickup.get_teams()
    for team in teams:
        filtered_members = [
            member['user']['role'] for member in team['members'] if member['user']['id'] == user_data['id']
        ]
        if len(filtered_members) > 0:
            user_role = filtered_members[0]

            await webhook_contoller.init_connection(token_data['access_token'], team['id'])

            break

    if user_role is None:
        user_role = Teams.not_set.value

    user_data['role'] = user_role

    await bind_data(user_id, prepare_user_data(user_data, token_data))


async def get_user_tasks(user_data: UserData, assigned_user_id: str = None) -> ClickUpTasks:
    """
    Получение списка задач на пользователя.

    Возвращается список задач уже отсортированный по приоритету и по тегам.
    """
    if assigned_user_id is None:
        assigned_user_id = user_data.click_up.id

    data = await ClickUp(user_data.click_up.auth_token).collect_user_tasks(assigned_user_id)

    data.tasks.sort(
        key=lambda x: (
            Priority(x.priority).priority_value,
            [
                Tags(x.name).priority_value for x in x.tags
            ]
        ),
        reverse=True
    )

    return data


async def get_user_tasks_with_unset_time(user_data: UserData) -> Optional[ClickUpTasks]:
    """
    Получение списка задач у которых не проставлено время выполнения на пользователя
    """
    data = await get_user_tasks(user_data)
    if not data:
        return None

    data.tasks = [x for x in data.tasks if x.time_estimate is None]
    return data


async def get_members(user_data: UserData) -> UserGroups:
    users_group = UserGroups(
        owner=[], admin=[], member=[], guest=[]
    )

    teams = await ClickUp(user_data.click_up.auth_token).get_teams()

    for team in teams:
        members = [x['user'] for x in team['members']]
        members.sort(key=lambda x: x['username'])

        for member in members:
            member_data = ClickUpUser(id=member['id'], username=member['username'], email=member['email'])
            try:
                group = Teams(member['role'])
                getattr(users_group, group.name).append(member_data)
            except Exception:
                print("Wrong member", member)
                continue

    return users_group


async def get_lists_by_folder(user_data: UserData, folder_id: int) -> FolderData:
    clickup = ClickUp(user_data.click_up.auth_token)

    folder = await clickup.get_folder(folder_id)
    lists = await clickup.get_lists(folder_id)

    return FolderData(
        id=folder['id'],
        name=folder['name'],
        lists=[ListData(id=x['id'], name=x['name']) for x in lists]
    )


async def get_user_folders(user_data: UserData) -> ClickUpData:
    """
    Сбор всех папочных-списков по пользователю.

    Папочные-списки - области где хранятся таски ClickUp.
    """
    prepared_teams = []

    clickup = ClickUp(user_data.click_up.auth_token)

    teams = await clickup.get_teams()

    for team in teams:
        prepared_spaces = []

        spaces = await clickup.get_spaces(team['id'])
        for space in spaces:
            prepared_folders = []

            folders = await clickup.get_folders(space['id'])
            for folder in folders:
                prepared_folders.append(
                    FolderData(
                        id=folder['id'],
                        name=folder['name'],
                        lists=[]
                    )
                )

            prepared_spaces.append(
                SpaceData(
                    id=space['id'],
                    name=space['name'],
                    folders=prepared_folders
                )
            )

        prepared_teams.append(
            TeamData(
                id=team['id'],
                name=team['name'],
                spaces=prepared_spaces
            )
        )

    return ClickUpData(teams=prepared_teams)


async def create_task(user_data: UserData, list_id: int, task_data: ClickUpCreateTask):
    return await ClickUp(user_data.click_up.auth_token).create_task(list_id, task_data)


async def get_task_by_id(user_data: UserData, task_id: str, is_need_members: bool = True) -> tuple:
    clickup = ClickUp(user_data.click_up.auth_token)

    try:
        task = await clickup.get_task(task_id)
    except httpx.HTTPStatusError as exc:
        logging.error(f"{str(exc)}, {exc.response}")
        return None, []

    prepared_task = prepare_task(task)

    if is_need_members:
        members = await clickup.get_users_by_task(prepared_task.id)
        prepared_members = [
            MemberItem(
                id=x['id'], name=x['username']
            ) for x in members if x['id'] in [y['id'] for y in prepared_task.assigned]
        ]
    else:
        prepared_members = None
    return prepared_task, prepared_members


async def get_tasks(user_data: UserData, list_id: int, status: ClickUpTaskStatusType) -> ClickUpTasks:
    """Получение списка задач по листу."""
    data = await ClickUp(user_data.click_up.auth_token).collect_tasks(list_id, status)

    data.tasks.sort(
        key=lambda x: (
            Priority(x.priority).priority_value,
            [
                Tags(x.name).priority_value for x in x.tags
            ]
        ),
        reverse=True
    )

    return data


async def send_assignee_notification(
        assignee_user_id: int,
        task_id: str,
        assignee_type: ClickUpAssigneeTypes,
        creator: str,
) -> None:
    """
    Отправка уведомления об назначении или снятии исполнителя по задаче.

    :param assignee_user_id: ID-clickup пользователя на которого нацеленно событие.
    :param assignee_type: Тип уведомления. Add - добавление Remove - Удаление
    :param creator: Кто сделал это событие.
    """
    user_data = await get_click_up_user(assignee_user_id, get_owner_if_null=True)
    if not user_data:
        return

    # Т.к. происходит жесткая привязка пользователя из события списко причастных к задаче мы не собираем.
    # Отправляем сообщение единственному пользователю к которому относится событие.
    task, members = await get_task_by_id(user_data, task_id, is_need_members=False)
    response = prepare_response_notification_assignee(
        task=task,
        assignee_type=assignee_type,
        creator=creator
    )

    await bot.send_message(user_data.user_id, response, parse_mode=ParseMode.HTML)


async def send_comment_post_notification(
        click_user_id: int,
        task_id: str,
        comment: str,
        creator: str
) -> None:
    """
    Отправка уведомления об добавление комментарья к задаче с отметкой пользователя.

    :param click_user_id: ID-clickup пользователя кто сделал это событие.
    :param comment: Комментарий к задаче. На выходе обрезается до 1024 символов.
    :param creator: Кто сделал это событие.
    """
    user_data = await get_click_up_user(click_user_id, get_owner_if_null=True)
    if not user_data:
        return

    task, members = await get_task_by_id(user_data, task_id)
    response = prepare_response_notification_comment_post(
        task=task,
        comment=comment,
        creator=creator
    )

    # Так как у нас не жесткой привязки к опрд пользователю
    # мы делаем рассылку на всех кто причастен к этой задаче.
    for member in members:
        assignee = await get_click_up_user(member.id)
        if not assignee:
            continue
        if len(response) > 4096:
            await bot.send_file('html')
        await bot.send_message(assignee.user_id, response, parse_mode=ParseMode.HTML)
