import httpx
import logging
from typing import Optional

from pydantic import validate_arguments

from src.apps.users.logic import bind_data
from src.apps.users.schemas import UserData
from src.submodules.clickup.enums import PriorityEnumsByEmoji, TagsEnumsByEmoji, Teams
from src.submodules.clickup.schemas import (
    ClickUpTasks, UserGroups, ClickUpUser, TeamData, ClickUpTaskItem,
    ClickUpData, FolderData, ListData, SpaceData, ClickUpCreateTask, MemberItem
)
from src.submodules.clickup.serializer import prepare_user_data, prepare_task
from src.submodules.clickup.service import ClickUp, ClickUpOAuth


@validate_arguments
async def add_click_up_data_by_user(user_id: int, code: str) -> None:
    """Добавление данных из ClickUp пользователю."""
    token_data = await ClickUpOAuth().get_token(code)

    click_up_user_data = await ClickUp(token_data['access_token']).get_user()

    await bind_data(user_id, prepare_user_data(click_up_user_data, token_data))


async def get_user_tasks(user_data: UserData, assigned_user_id: str = None) -> Optional[ClickUpTasks]:
    """
    Получение списка задач на пользователя.

    Возвращается список задач уже отсортированный по приоритету и по тегам.
    """
    if assigned_user_id is None:
        assigned_user_id = user_data.click_up.id

    data = await ClickUp(user_data.click_up.auth_token).collect_user_tasks(assigned_user_id)

    data.tasks.sort(
        key=lambda x: (
            PriorityEnumsByEmoji(x.priority).priority_value,
            [
                TagsEnumsByEmoji(x.name).priority_value for x in x.tags
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


async def get_task_by_id(user_data: UserData, task_id: str) -> tuple:
    clickup = ClickUp(user_data.click_up.auth_token)

    try:
        task = await clickup.get_task(task_id)
    except httpx.HTTPStatusError as exc:
        logging.error(f"{str(exc)}, {exc.response}")
        return None, []

    prepared_task = prepare_task(task)

    members = await clickup.get_users_by_task(prepared_task.id)
    prepared_members = [
        MemberItem(
            id=x['id'], name=x['username']
        ) for x in members if x['id'] in [y['id'] for y in prepared_task.assigned]
    ]

    return prepared_task, prepared_members

