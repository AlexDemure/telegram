from .schemas import HubStaffTask, HubStaffActivity, HubStaffUserData


def prepare_task(task: dict) -> HubStaffTask:
    return HubStaffTask(
        id=task['id'],
        name=task['summary'],
    )


def prepare_activity(activity: dict, task: HubStaffTask) -> HubStaffActivity:
    return HubStaffActivity(
        task=task,
        activity=activity['overall'],
        tracked=activity['tracked'],
    )


def prepare_user_data(user_data: dict, token_data: dict) -> HubStaffUserData:
    return HubStaffUserData(
        id=user_data['id'],
        username=user_data['name'],
        email=user_data['email'],
        auth_token=f"Bearer {token_data['access_token']}",
        refresh_token=token_data['refresh_token']
    )
