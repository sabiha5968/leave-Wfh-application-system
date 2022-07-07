from sqlalchemy import create_engine,Column, Integer,String, Boolean, ForeignKey, CHAR,DateTime
from sqlalchemy.orm import relationship
from database import Base, engine
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Department(Base):
    __tablename__="department"

    id=Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
)
    name=Column(String)

class Employee(Base):
    __tablename__="employee"

    id=Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
)
    name=Column(String)
    address=Column(String)
    email_id=Column(String)
    department=Column(UUID,ForeignKey("department.id"))
    salary=Column(Integer)
    phone_number=Column(Integer)
    head=Column(Boolean)
    time=Column(DateTime(timezone=True))





Base.metadata.create_all(engine)
