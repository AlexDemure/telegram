from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.schemas.clickup import ClickUpUserData
from src.schemas.hubstaff import HubStaffUserData


class UserDataBase(BaseModel):
    user_id: int
    click_up: Optional[ClickUpUserData] = None
    hub_staff: Optional[HubStaffUserData] = None


class UserCreate(UserDataBase):
    registration_at: datetime


class UserData(UserDataBase):
    registration_at: datetime

