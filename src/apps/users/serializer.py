from src.schemas.users import UserData


def prepare_user_data(data: dict) -> UserData:
    return UserData(
        user_id=data['user_id'],
        registration_at=data['registration_at'],
        click_up=data['click_up'],
        hub_staff=data['hub_staff'],
    )
