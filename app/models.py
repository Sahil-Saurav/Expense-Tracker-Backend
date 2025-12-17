from datetime import datetime,date
from sqlalchemy import Column,Integer,Float,String,DateTime,ForeignKey,Enum,Date
from sqlalchemy.orm import mapped_column,relationship,Mapped
from sqlalchemy.sql import func
from app.database import Base
from app.enums import TransactionTypes,Gender
from typing import List

class User(Base):

    __tablename__ = "user"

    u_id : Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    u_name : Mapped[str] = mapped_column(String)
    u_email : Mapped[str] = mapped_column(String,unique=True,nullable=False)
    u_password : Mapped[str] = mapped_column(String,nullable=False)
    u_dob : Mapped[date] = mapped_column(Date,nullable=False)
    u_gender : Mapped[Gender] = mapped_column(Enum(Gender))
    created_At : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_At : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

    expenses: Mapped[list["Expenses"]] = relationship(
        "Expenses",
        back_populates="user_Details",
        cascade="all, delete-orphan"
    )

    debt_credit : Mapped[list["Debt"]] = relationship(
        "Debt",
        foreign_keys="Debt.creditor_id",
        back_populates="creditor_details",
        cascade="all, delete-orphan"
    )

    debt_active : Mapped[list["Debt"]] = relationship(
        "Debt",
        foreign_keys="Debt.debtor_id",
        back_populates="debtor_details",
        cascade="all, delete-orphan"
    )

class Expenses(Base):

    __tablename__ = "expenses"

    exp_id : Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    u_id : Mapped[int] = mapped_column(ForeignKey("user.u_id"))
    amount : Mapped[float] = mapped_column(Float)
    type : Mapped[TransactionTypes] = mapped_column(Enum(TransactionTypes),nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    created_At : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_At : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

    user_Details : Mapped["User"] = relationship(
        "User",
        back_populates="expenses"
        )
    
class Debt(Base):

    __tablename__ = "debt"

    d_id : Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    creditor_id : Mapped[int] = mapped_column(ForeignKey("user.u_id"))
    debtor_id : Mapped[int] = mapped_column(ForeignKey("user.u_id"))
    amount : Mapped[float] = mapped_column(Float,nullable=False)
    purpose : Mapped[str] = mapped_column(String,nullable=True)
    interest : Mapped[float] = mapped_column(Float,nullable=False,default=0.0)
    issued_date : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    due_date : Mapped[date] = mapped_column(Date,nullable=False)

    creditor_details : Mapped["User"] = relationship(
        "User",
        foreign_keys=[creditor_id],
        back_populates="debt_credit"
    )
    debtor_details : Mapped["User"] = relationship(
        "User",
        foreign_keys=[debtor_id],
        back_populates="debt_active"
    )