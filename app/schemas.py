from pydantic import BaseModel,ConfigDict,field_validator,computed_field
from typing import List
from datetime import datetime,date
from app.enums import TransactionTypes,Gender

def calculate_age(dob: date) -> int:
    today = date.today()
    return (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))


class Create_User(BaseModel):
    u_name:str
    u_email:str
    u_password:str
    u_dob: str  # expecting DD/MM/YYYY
    u_gender : Gender

    @field_validator("u_dob")
    @classmethod
    def validate_dob(cls, v: str) -> date:
        try:
            return datetime.strptime(v, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("DOB must be in DD/MM/YYYY format")

class Update_User(BaseModel):
    u_name:str|None = None
    u_email:str|None = None
    u_gender : Gender|None = None

class Change_Password(BaseModel):
    old_password:str
    new_password:str

class Update_DOB(BaseModel):
    u_dob : str

    @field_validator("u_dob")
    @classmethod
    def validate_dob(cls, v: str) -> date:
        try:
            return datetime.strptime(v, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("DOB must be in DD/MM/YYYY format")
            


class Show_User(BaseModel):
    u_id:int
    u_name:str
    u_email:str
    u_gender : Gender
    u_dob : date
    created_At:datetime
    updated_At:datetime

    @computed_field
    @property
    def u_age(self) -> int:
        today = date.today()
        return today.year - self.u_dob.year - ((today.month, today.day) < (self.u_dob.month, self.u_dob.day))

    model_config = ConfigDict(from_attributes=True)

class Expense_User(BaseModel):
    u_id:int
    u_name:str
    u_email:str


class Create_Expense(BaseModel):
    u_id : int
    amount : float
    type : TransactionTypes
    description : str|None = None

class Show_Expense(BaseModel):
    exp_id: int
    amount :float
    type : TransactionTypes
    description : str|None = None
    created_At : datetime
    updated_At : datetime
    user_Details : Expense_User

    model_config = ConfigDict(from_attributes=True)

class Show_User_Expense(BaseModel):
    exp_id : int
    amount : float
    type : TransactionTypes
    description : str
    created_At : datetime
    updated_At : datetime

class Update_Expense(BaseModel):
    amount : float
    type : TransactionTypes|None = None
    description : str|None = None

class Create_Debt(BaseModel):
    amount : float
    purpose : str|None = None
    interest : float
    due_date : str

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: str) -> date:
        try:
            return datetime.strptime(v, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("Due Date must be in DD/MM/YYYY format")

class Show_Debt_Details(BaseModel):
    d_id : int
    creditor_id : int
    debtor_id : int
    amount : float
    purpose : str
    interest : float
    issued_date : datetime
    due_date : date
    creditor_details : Show_User
    debtor_details : Show_User

    model_config = ConfigDict(from_attributes=True)

class Show_Debt_On_User(BaseModel):
    d_id : int
    creditor_id : int
    debtor_id : int
    amount : float
    purpose : str
    interest : float
    issued_date : datetime
    due_date : date
    creditor_details : Show_User

    model_config = ConfigDict(from_attributes=True)

class Show_Credit_On_User(BaseModel):
    d_id : int
    creditor_id : int
    debtor_id : int
    amount : float
    purpose : str
    interest : float
    issued_date : datetime
    due_date : date
    debtor_details : Show_User

    model_config = ConfigDict(from_attributes=True)