from .schemas import HubStaffTask, HubStaffActivity


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

