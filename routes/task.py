from datetime import datetime
from fastapi import APIRouter, Response
from config.db import conn
from models.task import tasks
from schemas.task import Task
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
            "created_at": task.created_at
        }
        for task in tasks_data
    ]


@task.post("/tasks", response_model=Task)
def create_task(task: Task):
    new_task = {
        "title": task.title,
        "description": task.description,
        "created_at": datetime.now()
    }
    result = conn.execute(tasks.insert().values(new_task))
    conn.commit()
    result_id = result.lastrowid

    created_task = conn.execute(tasks.select().where(
        tasks.c.id == result_id)).fetchone()

    if created_task:
        return {
            "id": created_task.id,
            "title": created_task.title,
            "description": created_task.description,
            "created_at": created_task.created_at
        }
    else:
        return Response(status_code=HTTP_404_NOT_FOUND)


@task.get("/tasks/{id}", response_model=Task)
def get_task(id: int):

    found_task = conn.execute(
        tasks.select().where(tasks.c.id == id)).fetchone()

    if found_task:
        return {
            "id": found_task.id,
            "title": found_task.title,
            "description": found_task.description,
            "created_at": found_task.created_at
        }
    else:
        return Response(status_code=HTTP_404_NOT_FOUND)


@task.put("/tasks/{id}", response_model=Task)
def update_task(id: int, task: Task):

    updated_task = {
        "title": task.title,
        "description": task.description,
        "updated_at": datetime.now()
    }

    result = conn.execute(tasks.update().values(title=updated_task["title"],
                                                description=updated_task["description"],
                                                updated_at=updated_task["updated_at"]).where(
        tasks.c.id == id))
    conn.commit()

    if result.rowcount == 0:
        raise Response(status_code=HTTP_404_NOT_FOUND)

    updated_task_data = conn.execute(tasks.select().where(
        tasks.c.id == id)).fetchone()

    return {
        "id": updated_task_data.id,
        "title": updated_task_data.title,
        "description": updated_task_data.description,
        "created_at": updated_task_data.created_at,
        "updated_at": updated_task_data.updated_at
    }


@task.delete("/tasks/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_task(id: int):

    conn.execute(tasks.delete().where(tasks.c.id == id))
    conn.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
