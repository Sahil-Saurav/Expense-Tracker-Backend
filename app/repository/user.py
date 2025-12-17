from .. import models,schemas,hash
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repository.util import get_user


def create_User(payload:schemas.Create_User,db:Session):
    existing = db.query(models.User).filter(models.User.u_email == payload.u_email).first()

    if existing :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists!!")

    new_user = models.User(u_name = payload.u_name,
                           u_email = payload.u_email,
                           u_password = hash.hashPassword(payload.u_password),
                           u_dob = payload.u_dob,
                           u_gender = payload.u_gender
                           )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def show_User(db:Session,id:int|None = None,email:str|None = None):

    user = get_user(models.User,db,id,email)

    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User doesn't exist,create a new account")
    
    return user

def update_User(payload: schemas.Update_User,db: Session,id: int | None = None,email: str | None = None):

    user = get_user(models.User,db,id,email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )

    update_data = payload.model_dump(exclude_unset=True)

    if "u_email" in update_data:
        existing_user = db.execute(
            select(models.User).where(
                models.User.u_email == update_data["u_email"],
            )
        ).scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return {"message": "Updated successfully"}

def change_Password(payload: schemas.Change_Password,db: Session,id: int | None = None,email: str | None = None):

    user = get_user(models.User,db,id,email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not hash.verifyHashPassword(payload.old_password, user.u_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect old password"
        )

    if hash.verifyHashPassword(payload.new_password, user.u_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be same as old password"
        )
    
    user.u_password = hash.hashPassword(payload.new_password)

    db.commit()
    db.refresh(user)

    return {"message": "Password updated successfully"}

def update_DOB(payload:schemas.Update_DOB,db:Session,id:int|None = None,email:str|None = None):
    user = get_user(models.User,db,id,email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found!!")

    update_dob = payload.model_dump(exclude_unset=True)
    for field,value in update_dob.items():
        setattr(user,field,value)
    

    db.commit()
    db.refresh(user)

    return {"message":"The DOB is updated"}

def delete_User(db:Session,u_id:int|None = None,email:str|None = None):
    user = get_user(models.User,db,u_id,email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    debts = db.query(models.Debt).filter(models.Debt.debtor_id == user.u_id).all()

    if debts : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Can't remove the User as he has an active debt associated to his account,first clear all debt then try to remove account.")
    
    db.delete(user)
    db.commit()

    return {"message":"User account deleted permanently!!"}