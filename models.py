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
    name=Column(varchar)

class Employee(Base):
    __tablename__="employee"

    id=Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
)
    name=Column(varchar)
    address=Column(varchar)
    email_id=Column(varchar)
    department=Column(varchar)
    salary=Column(varchar)
    phone_number=Column(varchar)
    head=Boolean
    time=Column(DateTime(timezone=True))





Base.metadata.create_all(engine)
