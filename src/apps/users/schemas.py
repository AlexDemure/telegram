from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.submodules.clickup.schemas import ClickUpUserData
from src.submodules.hubstaff.schemas import HubStaffUserData


class UserDataBase(BaseModel):
    user_id: int
    fullname: str = "NOT_SET"
    username: str
    click_up: Optional[ClickUpUserData] = None
    hub_staff: Optional[HubStaffUserData] = None


class UserCreate(UserDataBase):
    registration_at: datetime


class UserData(UserDataBase):
    registration_at: datetime
