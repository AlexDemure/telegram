from aiohttp import web

from src.submodules.clickup.enums import ClickUpEvents, ClickUpAssigneeTypes
from src.apps.clickup.logic import send_assignee_notification, send_comment_post_notification


async def accept_notification(request):
    """Прием всех уведомлений из ClickUp."""
    payload = await request.json()

    if payload['event'] == ClickUpEvents.task_assignee.value:
        await notification_assignee_update(payload)

    elif payload['event'] == ClickUpEvents.comment_post.value:
        await notification_comment_post_update(payload)

    return web.json_response(status=200, data=dict(msg="OK"))


async def notification_assignee_update(payload: dict) -> None:
    """Работа с уведомление по обновлению исполнителя в задаче."""
    history = payload['history_items'][0]  # В таких событиях всегда передается 1 элемент в списке.

    assignee_type = ClickUpAssigneeTypes(history['field'])

    if assignee_type == ClickUpAssigneeTypes.add:
        user_id = history['after']['id']
    elif assignee_type == ClickUpAssigneeTypes.remove:
        user_id = history['before']['id']
    else:
        raise ValueError

    await send_assignee_notification(
        assignee_user_id=user_id,
        task_id=payload['task_id'],
        assignee_type=assignee_type,
        creator=history['user']['username']
    )


async def notification_comment_post_update(payload: dict) -> None:
    """Работа с уведомлением по добавлению комментарьев по задаче."""
    history = payload['history_items'][0]  # В таких событиях всегда передается 1 элемент в списке.

    # comments - может иметь 3 элемента
    # 1) Если указан в комментарии кому адресовано письмо или какое-то форматирование текста.
    # 2) Сам текст комментарья без учета адресата
    # 3) Отступы
    comments = history['comment']['comment']

    await send_comment_post_notification(
        click_user_id=history['user']['id'],
        task_id=payload['task_id'],
        comment=" ".join([x['text'] for x in comments]),
        creator=history['user']['username'],
    )
