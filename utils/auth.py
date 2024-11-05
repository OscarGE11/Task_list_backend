import os
from dotenv import load_dotenv
from fastapi import Cookie, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
import jwt
from schemas.user import UserResponse
from utils.generateToken import SECRET_KEY
from starlette.status import HTTP_401_UNAUTHORIZED

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
security = HTTPBearer()


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")
        email = payload.get("email")
        if user_id is None or email is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return UserResponse(id=user_id, email=email)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
