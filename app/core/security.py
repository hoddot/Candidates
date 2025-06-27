from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
import secrets
from fastapi import HTTPException, status, Header
from dotenv import load_dotenv
import os
import random
import string

load_dotenv()


# ใช้สำหรับการเข้ารหัส password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key สำหรับการเข้ารหัส JWT
# SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # เวลาหมดอายุของ Access Token
REFRESH_TOKEN_EXPIRE_DAYS = 7    # เวลาหมดอายุของ Refresh Token (7 วัน)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def random_password(length = 8):
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    hashed_password = get_password_hash(password)
    
    return { "password": password, "hashed_password": hashed_password }

# ฟังก์ชันในการสร้าง access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    to_encode.update({"token_type": "access"})
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ฟังก์ชันในการสร้าง refresh token
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    to_encode.update({"token_type": "refresh"})
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)  # หมดอายุใน 7 วัน
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ฟังก์ชันในการตรวจสอบ token (access token)
def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing"
        )

    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(status_code=403, detail="Token expired")
        if payload.get("token_type") != "access":
            raise HTTPException(status_code=403, detail="Invalid token type")
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired"
        )
    except jwt.JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid token: {str(e)}"
        )


# ฟังก์ชันในการตรวจสอบ refresh token
def verify_refresh_token(refresh_token: str) -> dict:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token type"
            )

        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token expired"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh token expired"
        )
    except jwt.JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid refresh token: {str(e)}"
        )