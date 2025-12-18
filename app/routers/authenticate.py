from ..repository import authenticate
from ..database import get_db
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=["Authentication"]
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    return authenticate.authenticate_User(request,db)