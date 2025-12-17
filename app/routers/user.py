from ..repository import user
from ..database import get_db
from ..schemas import Create_User,Show_User,Update_User,Change_Password,Update_DOB
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post('/create',response_model=Show_User,status_code=status.HTTP_201_CREATED)
def create_User(payload:Create_User,db:Session = Depends(get_db)):
    return user.create_User(payload,db)

@router.get('/get',response_model=Show_User,status_code=status.HTTP_200_OK)
def get_User(db:Session = Depends(get_db),id:int|None = None,email:str|None = None):
    return user.show_User(db,id,email)

@router.put('/update_user_details',status_code=status.HTTP_202_ACCEPTED)
def update_User(payload:Update_User,db:Session = Depends(get_db),id:int|None = None,email:str|None = None):
    return user.update_User(payload,db,id,email)

@router.put('/change_password',status_code=status.HTTP_202_ACCEPTED)
def change_Password(payload:Change_Password,db:Session=Depends(get_db),id:int|None = None,email:str|None = None):
    return user.change_Password(payload,db,id,email)

@router.put('/change_dob',status_code=status.HTTP_202_ACCEPTED)
def update_DOB(payload:Update_DOB,db:Session=Depends(get_db),id:int|None = None,email:str|None = None):
    return user.update_DOB(payload,db,id,email)

@router.delete('/delete_user',status_code=status.HTTP_200_OK)
def delete_User(db:Session = Depends(get_db),u_id:int|None = None,email:str|None = None):
    return user.delete_User(db,u_id,email)