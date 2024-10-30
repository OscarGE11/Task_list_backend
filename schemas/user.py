from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: Optional[int]
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True
