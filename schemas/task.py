from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TaskCreate(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
