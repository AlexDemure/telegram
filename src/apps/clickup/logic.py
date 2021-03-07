from typing import Optional

from pydantic import validate_arguments

from src.apps.users.logic import bind_data
from src.apps.users.schemas import UserData
from src.submodules.clickup.enums import PriorityEnumsByEmoji, TagsEnumsByEmoji
from src.submodules.clickup.schemas import ClickUpTasks
from src.submodules.clickup.serializer import prepare_user_data
from src.submodules.clickup.service import ClickUp, ClickUpOAuth


@validate_arguments
async def add_click_up_data_by_user(user_id: int, code: str) -> None:
    """Добавление данных из ClickUp пользователю."""
    token_data = await ClickUpOAuth().get_token(code)

    click_up_user_data = await ClickUp(token_data['access_token']).get_user()

    await bind_data(user_id, prepare_user_data(click_up_user_data, token_data))


async def get_user_tasks(user_data: UserData) -> Optional[ClickUpTasks]:
    """
    Получение списка задач на пользователя.

    Возвращается список задач уже отсортированный по приоритету и по тегам.
    """
    data = await ClickUp(user_data.click_up.auth_token).collect_user_tasks(user_data.click_up.id)

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
