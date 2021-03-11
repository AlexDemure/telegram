from typing import List
from src.submodules.clickup.enums import Priority, Tags, ClickUpAssigneeTypes
from src.submodules.clickup.schemas import ClickUpTasks, ClickUpTaskItem, MemberItem
from src.submodules.clickup.serializer import tags_list_to_emoji_str


def prepare_response_list_tasks(data: ClickUpTasks) -> str:
    """Подготовка данных для ответа в телеграмм."""
    response = f"Список задач:\n"
    for task in data.tasks:
        tags_to_str = tags_list_to_emoji_str(task.tags)
        priority_to_emoji = Priority(task.priority).emoji
        response += f"{priority_to_emoji}{tags_to_str} <a href='{task.url}'>{task.id}</a> {task.name}\n"

    return response[:4096]


def prepare_response_list_tasks_with_unset_time(data: ClickUpTasks) -> str:
    """Подготовка данных для ответа в телеграмм."""
    response = f"Не проставлено планируемое время в задачах:\n"
    for task in data.tasks:
        response += f"<a href='{task.url}'>{task.id}</a> {task.name}\n"

    return response[:4096]


def prepare_response_create_task_check_data(task_data: dict) -> str:
    """Подготовка ответа для проверки данных при создании задачи."""
    response = f"Проверка данных\n"
    response += f"Область: {task_data['folder_name']} - {task_data['list_name']}\n"
    response += f"Название: {task_data['name']}\n"

    if len(task_data['desc']) > 128:
        response += f"Описание: {task_data['desc'][:128]}...\n"
    else:
        response += f"Описание: {task_data['desc']}\n"

    response += f"Исполнитель: {task_data['click_up_username']}\n"

    tags_to_str = ""
    for tag in task_data['tags']:
        tags_to_str += f"{Tags(tag).preview_name} "
    response += f"Теги: {tags_to_str}\n"

    response += f"Приоритет: {Priority(task_data['priority']).preview_name}\n"

    return response[:4096]


def prepare_response_task_data(task: ClickUpTaskItem, members: List[MemberItem]) -> str:
    """Подготовка ответа для полученя данных по задаче."""
    tags_to_str = tags_list_to_emoji_str(task.tags)
    priority_to_emoji = Priority(task.priority).emoji

    if len(members) > 0:
        assigned = ', '.join([x.name for x in members])
    else:
        assigned = "Не назначено"

    return f"Инфомарция по задаче\n" \
           f"<b>Область: {task.folder_name} | {task.list_name}</b>\n" \
           f"Информация: {priority_to_emoji}{tags_to_str} <a href='{task.url}'>{task.id}</a> {task.name}\n" \
           f"Исполнитель: {assigned}"


def prepare_response_notification_assignee(
        task: ClickUpTaskItem,
        assignee_type: ClickUpAssigneeTypes,
        creator: str
) -> str:
    """Подготовка ответа для уведомления по назначению и снятии исполнителя по задаче"""
    response = "<b>Уведомление</b>\n"
    if assignee_type == ClickUpAssigneeTypes.add:
        response += f"{creator} назначил на вас задачу\n"
    elif assignee_type == ClickUpAssigneeTypes.remove:
        response += f"{creator} снял c вас задачу\n"
    else:
        raise ValueError

    tags_to_str = tags_list_to_emoji_str(task.tags)
    priority_to_emoji = Priority(task.priority).emoji
    response += f"{priority_to_emoji}{tags_to_str} <a href='{task.url}'>{task.id}</a> {task.name}\n"

    return response[:4096]


def prepare_response_notification_comment_post(
        task: ClickUpTaskItem,
        comment: str,
        creator: str
) -> str:
    """Подготовка ответа для уведомления по добавлению комментарья к задаче."""
    response = f"<b>Уведомление</b>\n{creator} добавил комментарий по задаче:\n"
    tags_to_str = tags_list_to_emoji_str(task.tags)
    priority_to_emoji = Priority(task.priority).emoji
    response += f"{priority_to_emoji}{tags_to_str} <a href='{task.url}'>{task.id}</a> {task.name}\n\n"

    response += f"<i>{comment[:1024]}</i>"

    return response[:4096]
