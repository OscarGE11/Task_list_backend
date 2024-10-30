import bcrypt
from fastapi import APIRouter, HTTPException
from sqlalchemy import delete, select, update

from config.db import conn
from schemas.user import User, UserCreate, UserResponse, UserUpdate
from models.user import users
from models.task import tasks
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED

user = APIRouter()


@user.post("/register", response_model=UserResponse)
def register(user: UserCreate):

    existing_user = conn.execute(select(users).where(
        users.c.email == user.email)).fetchone()

    if existing_user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="User already exists")

    hashed_password = bcrypt.hashpw(user.password.encode(
        "utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = {
        "email": user.email,
        "password": hashed_password
    }

    result = conn.execute(users.insert().values(
        new_user).returning(users.c.id)).fetchone()
    conn.commit()

    new_user_id = result.id

    return UserResponse(id=new_user_id, email=user.email)


@user.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: int):

    conn.execute(delete(tasks).where(tasks.c.user_id == user_id))

    result = conn.execute(users.delete().where(users.c.id == user_id))
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Task not found")


@user.get("/users", response_model=list[UserResponse])
def get_users():
    users_data = conn.execute(select(users)).fetchall()
    return [
        {
            "id": user.id,
            "email": user.email
        }
        for user in users_data
    ]


@user.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):

    found_user = conn.execute(select(users).where(
        users.c.id == user_id)).fetchone()
    if found_user:
        return {
            "id": found_user.id,
            "email": found_user.email
        }
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not found")


@user.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):

    current_user = conn.execute(select(users).where(
        users.c.id == user_id)).fetchone()

    if not current_user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not found")

    update_values = {}

    if user.email is not None:
        update_values['email'] = user.email

    if update_values:
        stmt = (
            update(users).
            where(users.c.id == user_id).
            values(**update_values)
        )
        conn.execute(stmt)
        conn.commit()

    user_id = current_user[0]
    user_email = update_values['email'] if 'email' in update_values else current_user[1]
    return UserResponse(id=user_id, email=user_email)
