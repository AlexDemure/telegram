from .schemas import UserData, TeamData, TaskItem, TagItem
from .enums import TagsEnumsByEmoji


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
        ] if task['tags'] else [],
        priority=task['priority']['priority'] if task['priority'] else "NOT_SET",
        url=task['url'],
        folder_name=task['folder']['name'],
        list_name=task['list']['name'],
    )
