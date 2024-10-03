from fastapi import FastAPI
from routes.task import task


app = FastAPI()

app.include_router(task)
