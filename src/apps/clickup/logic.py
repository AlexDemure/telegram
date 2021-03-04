from typing import Optional

from src.apps.clickup.enums import PriorityEnumsByEmoji, TagsEnumsByEmoji
from src.apps.clickup.service import ClickUp
from src.schemas.clickup import ClickUpTasks
from src.schemas.users import UserData


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
