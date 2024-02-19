from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    status = Column(String)
    created_on = Column(Date)
    experiences = relationship("Experience", back_populates="employee")

class Experience(Base):
    __tablename__ = 'experience'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    company_name = Column(String)
    role = Column(String)
    date_of_joining = Column(Date)
    last_date = Column(Date)
    employee = relationship("Employee", back_populates="experiences")