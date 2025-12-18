from app.hash import verifyHashPassword
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import models,schemas,token
import os
from pathlib import Path
from datetime import  timedelta

def authenticate_User(request:OAuth2PasswordRequestForm,db:Session):
    
    user = db.query(models.User).filter(models.User.u_email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not verifyHashPassword(request.password,user.u_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect Password")
    access_token_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',"30"))
    access_token_expires = timedelta(minutes=access_token_minutes)
    access_token = token.create_access_token(
        data={"sub": user.u_email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
