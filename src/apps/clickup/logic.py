from typing import Optional
from pydantic import validate_arguments

from src.apps.users.logic import bind_click_up
from src.core.sessions import HTTP_CLIENT
from src.apps.users.schemas import UserData
from src.submodules.clickup.enums import PriorityEnumsByEmoji, TagsEnumsByEmoji
from src.submodules.clickup.schemas import ClickUpTasks, ClickUpUserData
from src.submodules.clickup.service import ClickUp, ClickUpOAuth


@validate_arguments
async def add_click_up_data_by_user(user_id: int, verify_code: str) -> None:
    """Добавление данных из ClickUp пользователю."""

    auth_token = await ClickUpOAuth(HTTP_CLIENT).get_auth_token(verify_code)
    click_up_user_data = await ClickUp(HTTP_CLIENT, auth_token).get_user()

    click_up_data = ClickUpUserData(
        id=click_up_user_data['id'],
        username=click_up_user_data['username'],
        email=click_up_user_data['email'],
        auth_token=auth_token

    )
    await bind_click_up(user_id, click_up_data)


async def get_user_tasks(user_data: UserData) -> Optional[ClickUpTasks]:
    """
    Получение списка задач на пользователя.

    Возвращается список задач уже отсортированный по приоритету и по тегам.
    """
    data = await ClickUp(
        HTTP_CLIENT, user_data.click_up.auth_token
    ).collect_user_tasks(user_data.click_up.id)

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
