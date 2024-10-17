from datetime import datetime
from fastapi import APIRouter, HTTPException, Response
from config.db import conn
from models.task import tasks
from schemas.task import Task, TaskCreate, TaskUpdate
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
task = APIRouter()


@task.get("/tasks", response_model=list[Task])
def get_tasks():
    tasks_data = conn.execute(tasks.select()).fetchall()

    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "is_done": task.is_done
        }
        for task in tasks_data
    ]


@task.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    new_task = {
        "title": task.title,
        "description": task.description,
        "created_at": datetime.now()
    }
    result = conn.execute(tasks.insert().values(
        new_task).returning(tasks.c.id))
    conn.commit()
    result_id = result.lastrowid

    result_id = result.fetchone()[0]

    created_task = conn.execute(tasks.select().where(
        tasks.c.id == result_id)).fetchone()

    if created_task:
        return {
            "id": created_task.id,
            "title": created_task.title,
            "description": created_task.description,
            "created_at": created_task.created_at,
            "updated_at": created_task.updated_at,
            "is_done": created_task.is_done
        }
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Task not found")


@task.get("/tasks/{id}", response_model=Task)
def get_task(id: int):
    found_task = conn.execute(
        tasks.select().where(tasks.c.id == id)).fetchone()

    if found_task:
        return {
            "id": found_task.id,
            "title": found_task.title,
            "description": found_task.description,
            "created_at": found_task.created_at,
            "updated_at": found_task.updated_at,
            "is_done": found_task.is_done
        }
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Task not found")


@task.put("/tasks/{id}", response_model=Task)
def update_task(id: int, task: TaskUpdate):

    db_task = conn.execute(tasks.select().where(tasks.c.id == id)).fetchone()

    if db_task is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Task not found")

    updated_task = {
        "title": task.title if task.title is not None else db_task.title,
        "description": task.description if task.description is not None else db_task.description,
        "is_done": task.is_done if task.is_done is not None else db_task.is_done,
        "updated_at": datetime.now()
    }

    result = conn.execute(tasks.update().values(
        updated_task).where(tasks.c.id == id))
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="Task not found")

    updated_task_data = conn.execute(tasks.select().where(
        tasks.c.id == id)).fetchone()

    return {
        "id": updated_task_data.id,
        "title": updated_task_data.title,
        "description": updated_task_data.description,
        "created_at": updated_task_data.created_at,
        "updated_at": updated_task_data.updated_at,
        "is_done": updated_task_data.is_done
    }


@task.delete("/tasks/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_task(id: int):

    result = conn.execute(tasks.delete().where(tasks.c.id == id))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Task not found")
