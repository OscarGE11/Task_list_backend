from fastapi import FastAPI
from routes.user import user
from routes.task import task
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://taskit-lemon.vercel.app", "http://localhost:3000"
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
