from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_done: bool = False

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None

    class Config:
        orm_mode = True
