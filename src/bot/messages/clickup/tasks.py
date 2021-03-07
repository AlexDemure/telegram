from src.submodules.clickup.enums import PriorityEnumsByEmoji
from src.submodules.clickup.schemas import ClickUpTasks
from src.submodules.clickup.serializer import tags_list_to_emoji_str


def prepare_response_list_tasks(data: ClickUpTasks) -> str:
    """Подготовка данных для ответа в телеграмм."""
    response = f"Список задач:\n"
    for task in data.tasks:
        tags_to_str = tags_list_to_emoji_str(task.tags)
        priority_to_emoji = PriorityEnumsByEmoji(task.priority).emoji
        response += f"{priority_to_emoji}{tags_to_str} <a href='{task.url}'>{task.id}</a> {task.name}\n"

    return response[:4096]


def prepare_response_list_tasks_with_unset_time(data: ClickUpTasks) -> str:
    """Подготовка данных для ответа в телеграмм."""
    response = f"Не проставлено планируемое время в задачах:\n"
    for task in data.tasks:
        response += f"<a href='{task.url}'>{task.id}</a> {task.name}\n"

    return response[:4096]
