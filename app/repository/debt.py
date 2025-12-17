from .. import models,schemas,hash
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..repository import util
from datetime import datetime

def create_Debt(payload:schemas.Create_Debt,db:Session,creditor_id : int|None = None,debtor_id : int|None = None,creditor_email : str|None = None,debtor_email : str|None = None):
    
    creditor = util.get_user(models.User,db,creditor_id,creditor_email)
    debtor = util.get_user(models.User,db,debtor_id,debtor_email)
    issued_date = datetime.utcnow().date()

    if not creditor :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The creditor details is invalid!!")
    if not debtor :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The debtor details is invalid!!")
    if creditor.u_id == debtor.u_id : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="The debtor and creditor can't be same!!")
    if issued_date >= payload.due_date : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Check the due date its not valid as it is smaller than today's date")

    debt = models.Debt(
        creditor_id = creditor.u_id,
        debtor_id = debtor.u_id,
        amount = payload.amount,
        purpose = payload.purpose,
        interest = payload.interest,
        due_date = payload.due_date
    )

    db.add(debt)
    db.commit()
    db.refresh(debt)

    return {"message":f"Debt of amount : {payload.amount} is lended to {debtor.u_name} from {creditor.u_name}"}

def show_Debt(d_id:int,db:Session):

    debt = db.query(models.Debt).filter(models.Debt.d_id == d_id).first()

    if not debt : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No details found about debt id = {d_id}")
    
    return debt

def show_Debt_On_User(db:Session,debtor_id:int|None = None,email:str|None = None):
    user = util.get_user(models.User,db,debtor_id,email)
    
    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with user id: {debtor_id} not found!")

    debts = db.query(models.Debt).filter(models.Debt.debtor_id == debtor_id).all()

    if not debts : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No active debt")
    
    return debts

def show_Credit_On_User(db:Session,creditor_id:int|None = None,email:str|None = None):
    user = util.get_user(models.User,db,creditor_id,email)
    
    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with user id: {creditor_id} not found!")

    credits = db.query(models.Debt).filter(models.Debt.creditor_id == creditor_id).all()

    if not credits : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No active credit on other")
    
    return credits

def delete_Debt(d_id:int,db:Session):
    debt = db.query(models.Expenses).filter(models.Debt.d_id == d_id).first()

    if not debt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No records found with id = {d_id}")
    
    db.delete(debt)
    db.commit()

    return {"message":"Succesfully removed from the records!!"}
    