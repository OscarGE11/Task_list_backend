from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True