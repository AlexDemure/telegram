from src.apps.users.schemas import UserData


def prepare_user_data(data: dict) -> UserData:
    return UserData(
        user_id=data['user_id'],
        email=data['email'],
        clickup_token=data['clickup_token'],
        hubstaff_token=data['hubstaff_token'],
    )
