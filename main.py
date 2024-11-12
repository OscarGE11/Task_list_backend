from fastapi import FastAPI
from routes.user import user
from routes.task import task
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://task-list-backend-1uq7.onrender.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task)
app.include_router(user)
