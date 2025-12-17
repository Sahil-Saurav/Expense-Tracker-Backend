from ..repository import debt
from ..database import get_db
from ..schemas import Create_Debt,Show_Debt_Details,Show_Debt_On_User,Show_Credit_On_User
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix='/debt',
    tags=["Debt"]
)

@router.post('/create_debt',status_code=status.HTTP_201_CREATED)
def create_Debt(payload:Create_Debt,db:Session = Depends(get_db),creditor_id : int|None = None,debtor_id : int|None = None,creditor_email : str|None = None,debtor_email : str|None = None):
    return debt.create_Debt(payload,db,creditor_id,debtor_id,creditor_email,debtor_email)

@router.get('/show_debt',response_model=Show_Debt_Details,status_code=status.HTTP_200_OK)
def show_Debt(d_id:int,db:Session = Depends(get_db)):
    return debt.show_Debt(d_id,db)

@router.get('/show_debt_on_user',response_model=List[Show_Debt_On_User],status_code=status.HTTP_200_OK)
def show_Debt_On_User(db:Session = Depends(get_db),debtor_id:int|None = None,email:str|None = None):
    return debt.show_Debt_On_User(db,debtor_id,email)

@router.get('/show_credit_on_user',response_model=List[Show_Credit_On_User],status_code=status.HTTP_200_OK)
def show_Credit_On_User(db:Session = Depends(get_db),creditor_id:int|None = None,email:str|None = None):
    return debt.show_Credit_On_User(db,creditor_id,email)

@router.delete('delete_debt',status_code=status.HTTP_200_OK)
def delete_Debt(d_id:int,db:Session = Depends(get_db)):
    return debt.delete_Debt(d_id,db)