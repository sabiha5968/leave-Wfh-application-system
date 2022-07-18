from pydantic import BaseModel, root_validator, validate_email, ValidationError, parse_obj_as
from datetime import datetime,date
import uuid
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import sessionmaker
from models import Gender,status,application_types


class EmployeeRequest(BaseModel):
    id : str
    first_name : str
    last_name : str
    date_of_birth : date
    gender : Gender
    phone_number : str
    personal_email_id : str
    company_email_id : str
    address : str
    department_id : str
    is_department_head : bool
    reporting_manager : str
    leave_balance : str
    wfh_balance : str
    position : str

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
    id : str
    first_name : str
    last_name : str
    date_of_birth : date
    gender : str
    phone_number : str
    personal_email_id : str
    company_email_id : str
    address : str
    department_id : str
    is_department_head : bool
    reporting_manager : str
    leave_balance : int
    wfh_balance : int
    position : str




    class Config:
        orm_mode=True


class DepartmentRequest(BaseModel):
    department:str

    class Config:
        orm_mode=True



class DepartmentResponse(BaseModel):
    id : str
    department:str

    class Config:
        orm_mode = True 



class ApplicationRequest(BaseModel):
    employee_id : str
    application_type : application_types
    from_date : date
    to_date : date
    reason : str
    status : status
    balance_before_approval : int
    balance_after_approval : int

    class config:
        orm_mode = True



class Applicationresponse(BaseModel):
    id : str
    application_id : str
    application_type : application_types
    from_date : date
    to_date : date
    reason : str
    status : status
    balance_before_approval : int
    balance_after_approval : int

    class Config:
        orm_mode = True 



class Positionrequest(BaseModel):
    id : str
    position : str

    class config:
        orm_mode = True


class PositionReponse(BaseModel):
    id : uuid.UUID
    position : str

    class cofig:
         orm_mode = True

    
















    
