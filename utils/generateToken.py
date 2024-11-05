from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def create_token(user_data: dict):

    expiration = datetime.now() + timedelta(days=1)

    user_data.update({"exp": expiration.timestamp()})
    return jwt.encode(user_data, SECRET_KEY, algorithm="HS256")
