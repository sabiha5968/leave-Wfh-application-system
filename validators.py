from pydantic import BaseModel, root_validator, validate_email, ValidationError, parse_obj_as
from datetime import datetime
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, engine

from  models import Employee


SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
class EmployeeRequest(BaseModel):
    name : str
    email_id : str
    address : str
    department : str
    salary : int
    head : bool
    phone_number:str
    time: datetime = str(datetime.now())





    @root_validator
    def validate_email_field(cls,values):
        em=values.get("email_id")
        if em:
            validate_email(em)
        return values



    @root_validator
    def validate_mobile(cls,values):
        ph=values.get("phone_number")
        if len(ph)==10 and ph.isdigit():
            return values
        raise ValueError("not a valid mobile number")

class EmployeeResponse(BaseModel):
    id:uuid.UUID
    name:str
    email_id:str
    address:str
    department:str
    salary:float
    head:bool
    phone_number=str
    time:datetime = str(datetime.now())

    class Config:
        orm_mode=True

class DepartmentRequest(BaseModel):
    name:str

    class Config:
        orm_mode=True

class DepartmentResponse(BaseModel):
    id:uuid.UUID
    name:str

    class Config:
        orm_mode=True