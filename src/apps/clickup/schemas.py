from typing import List, Optional
from pydantic import BaseModel


class TagItem(BaseModel):
    name: str


class TaskItem(BaseModel):
    id: str
    name: str
    status: str
    assigned_name: str
    assigned_id: int
    tags: List[TagItem]
    priority: str
    url: str
    time_estimate: Optional[int]
    points: Optional[int]
    folder_name: str
    list_name: str


class UserData(BaseModel):
    id: int
    username: str
    email: str


class UserTasks(BaseModel):
    tasks: List[TaskItem]
    user: UserData


class TeamData(BaseModel):
    id: int
    name: str
