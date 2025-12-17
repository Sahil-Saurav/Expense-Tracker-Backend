from ..repository import expense
from ..database import get_db
from ..schemas import Create_Expense,Show_Expense,Show_User_Expense,Update_Expense
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix='/expense',
    tags=["Expense"]
)

@router.post('/add_expense',status_code=status.HTTP_201_CREATED)
def add_Expense(payload:Create_Expense,db:Session = Depends(get_db)):
    expense.add_Expense(payload,db)
    return "ok"

@router.get('/get_expense',response_model=Show_Expense,status_code=status.HTTP_200_OK)
def show_Expense(e_id:int,db:Session = Depends(get_db)):
    return expense.show_Expense(e_id,db)

@router.get('/get_user_expense',response_model=List[Show_User_Expense],status_code=status.HTTP_200_OK)
def show_User_Expense(u_id:int,db:Session = Depends(get_db)):
    return expense.show_User_Expense(u_id,db)

@router.put('/update_expense',status_code=status.HTTP_202_ACCEPTED)
def update_Expense(payload:Update_Expense,db:Session = Depends(get_db),e_id:int|None = None):
    return expense.update_Expense(payload,db,e_id)

@router.delete('/delete_expense',status_code=status.HTTP_200_OK)
def delete_Expense(e_id:int,db:Session = Depends(get_db)):
    return expense.delete_Expense(e_id,db)