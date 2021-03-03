from typing import Optional

from pydantic import BaseModel


class UserDataBase(BaseModel):
    user_id: int
    email: Optional[str] = None
    clickup_token: Optional[str] = None
    hubstaff_token: Optional[str] = None
    hubstaff_refresh_token: Optional[str] = None


class UserCreate(UserDataBase):
    pass


class UserData(UserDataBase):
    pass
