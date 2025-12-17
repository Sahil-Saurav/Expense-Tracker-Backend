from ..repository import util
from fastapi import APIRouter,status

router = APIRouter(
    prefix='/utilities',
    tags=['Utilities']
)

@router.get('/expense_types',status_code=status.HTTP_200_OK)
def show_Expense_Types():
    return util.show_Expense_Types()

@router.get('/gender_types',status_code=status.HTTP_200_OK)
def show_Gender_Types():
    return util.show_Gender_Types()