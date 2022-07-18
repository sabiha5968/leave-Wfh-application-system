 from sqlalchemy import create_engine,Column, Integer,String, DATE,Boolean, ForeignKey, CHAR,DateTime
from sqlalchemy.orm import relationship
from database import Base, engine
from datetime import datetime
import uuid  
from sqlalchemy.dialects.postgresql  import UUID, Enum, VARCHAR
from sqlalchemy import Enum
 
class Department(Base):
    __tablename__="department"

    id=Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
)
    name=Column(VARCHAR)

class Gender(str, Enum):
    Female = "1"
    Male = "2"
    Other = "3"

class Employee(Base):
    __tablename__="employee"

    id=Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuØid4,
)
    fist_name = Column(VARCHAR)
    last_name =Column(VARCHAR)
    date_of_birth =Column(DATE)
    gender = Column(Gender)
    phone_no = Column(String)
    personal_email_id = Column(VARCHAR)
    company_email_id = Column(VARCHAR)
    address = Column(VARCHAR)
    department_id = Column(String)
    is_department_head = Column(Boolean)
    reporting_manager = Column(VARCHAR)
    leave_balance = Column(String)
    wfh_balance = Column(String)
    position = Column(VARCHAR)




class Application(Base):
    __tablename__ = "application"

    id = Column( UUID (as_uuid = True),
        primary_key = True,
        default_key = uuid.uuid4,
)
    employee_id = Column(UUID(as_uuid = True), ForeignKey())
    application_type = Column(VARCHAR)
    from_date = Column(VARCHAR)
    to_date = Column(DATE)
    reason = Column(VARCHAR)
    status = Column(VARCHAR)
    balance_before_approval = Column(Integer)
    balance_after_approval = Column(Integer)

class Position(Base):
    __tablename__ = "position"

    id = uuid.uuid4
    position = Column(VARCHAR)

Base.metadata.create_all(engine)
