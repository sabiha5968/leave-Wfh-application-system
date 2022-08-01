from sqlalchemy import create_engine,Column, Integer,String, DATE,Boolean, ForeignKey, CHAR,DateTime
from sqlalchemy.orm import relationship
from database import Base, engine
from datetime import date
from uuid import uuid4
from sqlalchemy.dialects.postgresql  import UUID, ENUM , VARCHAR
import enum

class Gender(str, enum.Enum):
    Female = "1"
    Male = "2"
    Other = "3"


class ApplicationType(str, enum.Enum):
    leave = "1"
    work_from_home = "2"


class Status(str, enum.Enum):
    pending = "1"
    approved = "2"
    rejected = "3"


class Department(Base):
    __tablename__="department"

    id=Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4

)
    department=Column(VARCHAR)

class Position(Base):
    __tablename__ = "position"

    id = Column(UUID(as_uuid = True),primary_key = True, default= uuid4)
    position = Column(VARCHAR)
    employee = relationship("Employee", back_populates = "position")

class Employee(Base):
    __tablename__="employee"

    id=Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
)
    application = relationship("Application",backref = "employee")
    first_name = Column(VARCHAR)
    last_name =Column(VARCHAR)
    date_of_birth =Column(DATE)
    gender = Column(ENUM(Gender))
    phone_no = Column(VARCHAR)
    personal_email_id = Column(VARCHAR)
    company_email_id = Column(VARCHAR)
    address = Column(VARCHAR)
    department_id = Column(UUID(as_uuid=True), ForeignKey("department.id"))
    is_department_head = Column(Boolean)
    reporting_manager = Column(UUID(as_uuid=True) , ForeignKey('employee.id'))
    leave_balance = Column(Integer)
    wfh_balance = Column(Integer)
    position_id = Column(UUID(as_uuid=True) ,ForeignKey('position.id'))
    position = relationship("Position", back_populates = "employee")



class Application(Base):
    __tablename__ = "application"

    id = Column(UUID(as_uuid = True),
        primary_key = True,
        default = uuid4,
)
    employee_id = Column(UUID(as_uuid = True), 
        ForeignKey('employee.id'), 
        default=uuid4
    )
    application_type = Column(ENUM(ApplicationType))
    name = Column(VARCHAR)
    subject = Column(VARCHAR)
    from_date = Column(DATE)
    to_date = Column(DATE)
    reason = Column(VARCHAR)
    status = Column(ENUM(Status))
    balance_before_approval = Column(Integer)
    balance_after_approval = Column(Integer)
    position_id = Column(UUID(as_uuid= True))
    position = relationship("Employee", back_populates = "application")





