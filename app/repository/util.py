from ..enums import TransactionTypes,Gender
from ..models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException,status

from typing import Type
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User

def get_user(model: Type[User],db: Session,id: int | None = None,email: str | None = None):
    if id is None and email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either id or email must be provided"
        )

    stmt = select(model)

    if id is not None:
        stmt = stmt.where(model.u_id == id)
    else:
        stmt = stmt.where(model.u_email == email)

    return db.execute(stmt).scalar_one_or_none()


def show_Expense_Types():
    return [t.value for t in TransactionTypes]

def show_Gender_Types():
    return [t.value for t in Gender]
