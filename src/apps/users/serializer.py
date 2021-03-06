from src.apps.users.schemas import UserData


def prepare_user_data(data: dict) -> UserData:
    return UserData(
        user_id=data['user_id'],
        fullname=data['fullname'],
        username=data['username'],
        registration_at=data['registration_at'],
        click_up=data['click_up'],
        hub_staff=data['hub_staff'],
    )
