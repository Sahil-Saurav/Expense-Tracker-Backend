from .. import models,schemas,hash
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.enums import TransactionTypes

def add_Expense(payload:schemas.Create_Expense,db:Session):
    user = db.query(models.User).filter(models.User.u_id == payload.u_id).first()
    expense = models.Expenses(u_id = payload.u_id,amount=payload.amount,type=payload.type,description=payload.description,user_Details = user)

    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found!!")

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense

def show_Expense(e_id:int,db:Session):
    expense = db.query(models.Expenses).filter(models.Expenses.exp_id == e_id).first()

    if not expense :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Expense with id = {e_id}")
    return expense

def show_User_Expense(u_id:int,db:Session):
    
    expenses = db.query(models.Expenses).filter(models.Expenses.u_id == u_id).all()

    if not expenses :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No expense history for the user with id = {u_id}")
    
    return expenses

def update_Expense(payload:schemas.Update_Expense,db:Session,e_id:int|None = None):

    expense = db.query(models.Expenses).filter(models.Expenses.exp_id == e_id).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No expense exsits with id = {e_id}")
    
    update_expense = payload.model_dump(exclude_unset=True).items()

    for field,value in update_expense :
        setattr(expense,field,value)
    
    db.commit()
    db.refresh(expense)

    return {"message":"Expense Updated!!"}

def delete_Expense(e_id:int,db:Session):
    expense = db.query(models.Expenses).filter(models.Expenses.exp_id == e_id).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No records found with id = {e_id}")
    
    db.delete(expense)
    db.commit()

    return {"message":"Succesfully removed from the records!!"}