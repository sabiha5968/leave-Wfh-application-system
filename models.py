from sqlalchemy import create_engine,Column, Integer,String, DATE,Boolean, ForeignKey, CHAR,DateTime
from sqlalchemy.orm import relationship
from database import Base, engine
from datetime import date
from uuid import uuid4
from sqlalchemy.dialects.postgresql  import UUID, ENUM , VARCHAR
from sqlalchemy import Enum
 

class Gender(str, Enum):
    Female = "1"
    Male = "2"
    Other = "3"


class application_type(str, Enum):
    leave = "1"
    work_from_home = "2"


class status(str, Enum):
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


class Employee(Base):
    __tablename__="employee"

    id=Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
)
    application = relationship("application",backref = "employee")
    first_name = Column(VARCHAR)
    last_name =Column(VARCHAR)
    date_of_birth =Column(DATE)
    gender = Column(Gender)
    phone_no = Column(VARCHAR)
    personal_email_id = Column(VARCHAR)
    company_email_id = Column(VARCHAR)
    address = Column(VARCHAR)
    department_id = Column(UUID(as_uuid = True), ForeignKey("department.id"))
    is_department_head = Column(Boolean)
    reporting_manager = Column(VARCHAR, ForeignKey('employee.id'))
    leave_balance = Column(Integer)
    wfh_balance = Column(Integer)
    position_id = Column(UUID(as_uuid = True),ForeignKey('position.id'))
    position = relationship("position", back_populates = "employee")



class Application(Base):
    __tablename__ = "application"

    id = Column( UUID (as_uuid = True),
        primary_key = True,
        default_key = uuid4,
)
    employee_id = Column(UUID(as_uuid = True), ForeignKey('employee.id'), default=uuid4)
    application_type = Column(application_type)
    from_date = Column(DATE)
    to_date = Column(DATE)
    reason = Column(VARCHAR)
    status = Column(status)
    balance_before_approval = Column(Integer)
    balance_after_approval = Column(Integer)
    position = relationship("employee", back_populates = "application")




class Position(Base):
    __tablename__ = "position"

    id = Column(UUID (as_uuid = True),primary_key = True, default_key = uuid4)
    position = Column(VARCHAR)
    employee = relationship("employee", back_populates = "position")

Base.metadata.create_all(engine)
