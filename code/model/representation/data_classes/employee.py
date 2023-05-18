from sqlalchemy import Column, Integer, String, Float, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship

from model.representation.data_classes.setup import Base
from model.representation.data_classes.availability import Availability


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    task= Column(Integer)

    employee = relationship("Employee", back_populates="task")


class Weekly_max(Base):
    __tablename__ = 'weekly_max'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    week = Column(Integer)
    max = Column(Integer)
    
    employee = relationship("Employee", back_populates="weekly_maxs")

    def __init__(self, week, max) -> None:
        self.week = week
        self.max = max

    def __str__(self) -> str:
        return f"Week {self.week}: {self.max} hours"

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(100))
    last_name = Column(VARCHAR(100))
    wage = Column(Float)
    min_hours = Column(Integer)
    level = Column(Integer)
    location = Column(String) # Is dit geen location ID?
    
    availability = relationship("Availability", back_populates="employee", cascade="all, delete, delete-orphan")
    weekly_maxs = relationship("Weekly_max", back_populates="employee")
    task = relationship("Task", back_populates="employee")

    def __init__(self, first_name: str, last_name: str, availability, maximum:dict[int, int], min_hours: int, wage: float, level: int, tasks: list[int], location: str) -> None:
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.availability = availability
        self.wage = wage
        self.weekly_max = maximum
        self.min_hours = min_hours
        self.level = level
        self.tasks = tasks
        self.location = location

        self.name = f'{first_name} {last_name}'
        self.priority = 0
        self.init_availability(self.availability)
        
    def to_dict(self)-> dict:
        ''' app.py will use this dict to store info in the session. That info will be
            stored on the users side in a cookie, so it can be viewed. That is why
            I did not include wage here because it is not safe. If we later decide we need wage,
            we should consider hashing it'''
        
        employee = {'first_name': self.first_name, 'last_name': self.last_name, 'level': self.level, 'location': self.location}
        return employee
    
    def db_to_instance(self):
        self.init_id()
        self.init_availability(self.availability)
        self.init_weekly_max()
        self.init_tasks()
    
    def init_id(self)-> int:
        self.id = self.id
    
    def init_weekly_max(self)-> dict:
        ''' converts the list with strings from the database into weekly_max dicts'''
        self.weekly_max = {x.week: x.max for x in self.weekly_maxs}
        print(self.weekly_max) # weekly_maxs is a list from the database with string info

    def init_availability(self, av: list[Availability]) -> dict[int, list[Availability]]:
        availability_dict = {}
        
        for availability in av:
            weeknum = availability.start.isocalendar()[1]

            if weeknum not in availability_dict:
                availability_dict[weeknum] = []

            availability_dict[weeknum].append(availability)
        self.availability_dict = availability_dict

    def init_tasks(self):
        self.tasks = self.task

    """ Get """
    def get_name(self) -> str:
        return self.name

    def get_av(self) -> list[dict]:
        return self.availability

    def get_wage(self) -> float:
        return float(self.wage)

    def get_level(self) -> int:
        return self.level

    def get_tasks(self) -> int:
        return self.tasks

    def get_week_max_dict(self) -> dict[int, int]:
        return self.weekly_max

    def get_week_max(self, week) -> int:
        return self.weekly_max.get(week)

    def get_minimal_hours(self) -> int:
        return self.min_hours

    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id})"
    
