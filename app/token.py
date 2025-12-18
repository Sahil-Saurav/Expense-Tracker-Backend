from datetime import datetime, timedelta, timezone
from app.schemas import TokenData
import os
import jwt
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError
from pathlib import Path


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt

def verify_access_token(token:str,Credentials_Exception:HTTPException):
    try:
        payload = jwt.decode(token,os.getenv("SECRET_KEY"),algorithms=['HS256']
)
        email = payload.get('sub')
        if email is None:
            raise Credentials_Exception
        token_data = TokenData(email = email)
        return token_data
    except InvalidTokenError:
        raise Credentials_Exception
