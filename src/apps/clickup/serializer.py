from typing import List

from src.apps.clickup.enums import TagsEnumsByEmoji, PriorityEnumsByEmoji
from src.apps.clickup.schemas import UserData, TeamData, TaskItem, TagItem, UserTasks


def prepare_user_data(user_data: dict) -> UserData:
    return UserData(
        id=user_data['user']['id'],
        username=user_data['user']['username'],
        email=user_data['user']['email'],
    )


def prepare_team(team: dict) -> TeamData:
    return TeamData(id=team['id'], name=team['name'],)


def prepare_task(task: dict) -> TaskItem:
    return TaskItem(
        id=task['id'],
        name=task['name'],
        status=task['status']['status'],
        assigned_name=task['assignees'][0]['username'] if task['assignees'] else "NOT_SET",
        assigned_id=task['assignees'][0]['id'] if task['assignees'] else "NOT_SET",
        tags=[
            TagItem(name=x['name']) for x in task['tags'] if getattr(TagsEnumsByEmoji, x['name'], None)
        ] if task['tags'] else [],  # Отображаем лишь те теги которые есть у нас в Enums
        priority=task['priority']['priority'] if task['priority'] else "NOT_SET",
        url=task['url'],
        time_estimate=task['time_estimate'] if task['time_estimate'] else None,
        points=task['points'] if task['points'] else None,
        folder_name=task['folder']['name'],
        list_name=task['list']['name'],

    )


def tags_list_to_emoji_str(tags: List[TagItem]) -> str:
    """Преобразовывает список тегов в одну строку брав вместо названия тега его emoji."""
    tags_to_str = ""
    for tag in tags:
        try:
            tags_to_str += f"{TagsEnumsByEmoji(tag.name).emoji}"
        except ValueError:
            continue

    return tags_to_str


def prepare_response_list_tasks(data: UserTasks) -> str:
    """Подготовка данных для ответа в телеграмм."""
    response = f"<b>Список задач:</b>\n"
    for task in data.tasks:
        tags_to_str = tags_list_to_emoji_str(task.tags)
        priority_to_emoji = PriorityEnumsByEmoji(task.priority).emoji
        response += f"{priority_to_emoji}{tags_to_str} <a href='{task.url}'>{task.id}</a> {task.name}\n"

    return response[:4096]


def prepare_response_list_tasks_with_unset_time(data: UserTasks) -> str:
    """Подготовка данных для ответа в телеграмм."""
    response = f"<b>Не проставлено планируемое время в задачах:</b>\n"
    for task in data.tasks:
        response += f"<a href='{task.url}'>{task.id}</a> {task.name}\n"

    return response[:4096]
