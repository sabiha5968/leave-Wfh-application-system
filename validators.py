from pydantic import BaseModel, root_validator, validate_email, ValidationError, parse_obj_as
from datetime import datetime,date
import uuid
from typing import Union
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import sessionmaker
from models import Gender,Status,ApplicationType


class EmployeeRequest(BaseModel):
    first_name : str
    last_name : str | None
    date_of_birth : date | None
    gender : Gender
    phone_no : str
    personal_email_id : str
    company_email_id : str
    address : str
    department_id : uuid.UUID
    is_department_head : bool
    reporting_manager : uuid.UUID | None
    leave_balance : int
    wfh_balance : int
    position_id : uuid.UUID

    @root_validator
    def validate_email_field(cls,values):
        em=values.get("personal_email_id")
        if em:
            validate_email(em)
        em2 = values.get("company_email_id")
        if em2:
            validate_email(em2)
        ph=values.get("phone_no")
        if not(len(ph)==10) and not (ph.isdigit()):
            raise ValueError("not a valid mobile number")
        
        return values

    
    class Config:
        orm_mode=True

class EmployeeResponse(BaseModel):
    id : uuid.UUID | None
    first_name : str | None
    last_name : str | None
    date_of_birth : date | None
    gender : str | None
    phone_no : str | None
    personal_email_id : str | None
    company_email_id : str | None
    address : str | None
    department_id : uuid.UUID | None
    is_department_head : bool | None
    reporting_manager : uuid.UUID | None
    leave_balance : int | None
    wfh_balance : int | None
    position_id : uuid.UUID | None

    class Config:
        orm_mode=True


class DepartmentRequest(BaseModel):
    department: str

    class Config:
        orm_mode=True


class DepartmentResponse(BaseModel):
    id : uuid.UUID
    department : str | None

    class Config:
        orm_mode = True 


class ApplicationRequest(BaseModel):
    employee_id : uuid.UUID
    application_type : ApplicationType
    from_date : date
    subject:str
    to_date : date
    reason : str 


    class config:
        orm_mode = True



class ApplicationResponse(BaseModel):
    id :  uuid.UUID
    employee_id : uuid.UUID | None
    application_type : ApplicationType | None
    subject:str | None
    from_date : date | None
    to_date : date | None
    reason : str | None
    status : Status | None
    balance_before_approval : int | None
    balance_after_approval : int | None
    

    class Config:
        orm_mode = True 



class PositionRequest(BaseModel):
    position : str

    class Config:
        orm_mode = True


class PositionResponse(BaseModel):
    id : uuid.UUID
    position : str | None

    class Config:
        orm_mode = True

    
















    
