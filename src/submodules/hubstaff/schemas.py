from typing import Optional, List

from pydantic import BaseModel


class HubStaffUserData(BaseModel):
    id: int
    username: str
    email: str
    auth_token: Optional[str] = None
    refresh_token: Optional[str] = None


class HubStaffTask(BaseModel):
    id: int
    name: str


class HubStaffActivity(BaseModel):
    task: HubStaffTask
    activity: int  # Общее время активности пользователя
    tracked: int  # Общее время затреканного времени


class HubStaffTotalActivity(BaseModel):
    organization_id: int
    organization_name: str
    activities: List[HubStaffActivity]
    total_activity: int  # Общее время активности пользователя
    total_tracked: int  # Общее время затреканного времени


class HubStaffActivityReports(BaseModel):
    reports: List[HubStaffTotalActivity]
