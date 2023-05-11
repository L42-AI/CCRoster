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
        self.first_name = first_name
        self.last_name = last_name
        self.availability = availability
        self.availability_dict = self.sort_availability(availability)
        self.wage = wage
        self.weekly_max = maximum
        self.min_hours = min_hours
        self.level = level
        self.tasks = tasks
        self.location = location

        self.name = f'{first_name} {last_name}'
        self.priority = 0

    def sort_availability(self, av: list[Availability]) -> dict[int, list[Availability]]:
        availability_dict = {}
        
        for availability in av:
            weeknum = availability.start.isocalendar()[1]

            if weeknum not in availability_dict:
                availability_dict[weeknum] = []

            availability_dict[weeknum].append(availability)
        return availability_dict
    
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