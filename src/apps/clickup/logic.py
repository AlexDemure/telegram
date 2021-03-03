from typing import Optional

from src.apps.clickup.enums import PriorityEnumsByEmoji, TagsEnumsByEmoji
from src.apps.clickup.schemas import UserTasks
from src.apps.clickup.service import ClickUp
from src.apps.users.logic import get_user


async def get_user_tasks(user_id: int) -> Optional[UserTasks]:
    """
    Получение списка задач на пользователя.

    Возвращается список задач уже отсортированный по приоритету и по тегам.
    """
    user_data = await get_user(user_id)
    if not user_data:
        return None

    data = await ClickUp(user_data.clickup_token).collect_user_tasks()

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


async def get_user_tasks_with_unset_time(user_id: int) -> Optional[UserTasks]:
    """
    Получение списка задач у которых не проставлено время выполнения на пользователя
    """
    data = await get_user_tasks(user_id)
    if not data:
        return None

    data.tasks = [x for x in data.tasks if x.time_estimate is None]
    return data
