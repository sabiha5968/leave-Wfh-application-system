from pydantic import BaseModel, root_validator, validate_email, ValidationError, parse_obj_as
from datetime import datetime
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalcemy import create_engine, engine
 
from  models import Employee


SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
class EmployeeRequest(BaseModel):
    first_name = str
    last_name = str
    date_of_birth = str
    gender = str
    phone_number = str
    personal_email_id = str
    company_email_id = str
    address = str
    department_id = str
    is_department_head = str
    reporting_manager = str
    leave_balance = str
    wfh_balance = str
    position = str

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
    first_name = str
    last name = str
    date_of_birth = str
    gender = str
    phone_number = str
    personal_email_id = str
    company_email_id = str
    address = str
    department_id = str
    is_department_head = str
    reporting_manager = str
    leave_balance = str
    wfh_balance = str
    position = str



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
        orm_mode = True 



class ApplicationRequest(BaseModel):
    id = uuid.UUID
    application_type = str
    from_date = str
    to_date = str
    reason = str
    status = str

    class config:
        orm_mode = True



class Applicationresponse(BaseModel):
    id = uuid.UUID
    application_id = uuid.UUID
    application_type = str
    from_date = str
    to_date =str
    reason = str
    status = str
    balance_before_approval = str
    balance_after_approval = str

    class Config:
        orm_mode = True 



class Positionrequest(BaseModel):
    position = str

    class config:
        orm_mode = True


class PositionReponse(BaseModel):
    id = uuid.UUID
    position = str

    class cofig:
         orm_mode = True

    
















    
