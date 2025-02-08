from typing import AsyncGenerator  # 이 줄 추가
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config import settings  # SECRET_KEY가 포함되어 있다고 가정

security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Security(security)) -> int:
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        print("Decoded payload:", payload)  # 디버깅용 로그 출력
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: user_id not found")
        return user_id
    except jwt.PyJWTError as e:
        print("JWT decode error:", str(e))  # 디버깅용 로그 출력
        raise HTTPException(status_code=401, detail="Invalid token")
