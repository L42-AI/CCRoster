from datetime import date
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    wage = Column(Integer)
    min_hours = Column(Integer)
    level = Column(Integer)
    task = Column(Integer)
    location = Column(Integer)
    weekly_max = relationship("Weekly_max", back_populates='employee')
    availability = relationship("Availability", back_populates='employee')
    shifts = relationship("Shift", back_populates='employee')

class Weekly_max(Base):
    __tablename__ = 'weekly_max'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    week = Column(Integer)
    max = Column(Integer)
    employee = relationship("Employee", back_populates='weekly_max')

class Shift(Base):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(Integer)
    task = Column(Integer)

    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates='shifts')

    schedule_id = Column(Integer, ForeignKey('schedules.id'))
    schedule = relationship("Schedule", back_populates='shifts')

class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    employee = relationship("Employee", back_populates='availability')    

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))  # Optional, to give the schedule a name
    date_created = Column(DateTime, default=date.today())  # Timestamp of when the schedule was created
    shifts = relationship("Shift", back_populates='schedule')  # Moved the relationship here from outside the class


def insert_employee(employee: Employee):
    '''inserts employee into database'''

    