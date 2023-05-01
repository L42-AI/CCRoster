from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from representation.availability import Availability
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    name = Column(String)
    wage = Column(Float)
    weekly_max = Column(Integer)
    min_hours = Column(Integer)
    level = Column(Integer)
    tasks = Column(String)
    location = Column(String)
    priority = Column(Integer)

    availabilities = relationship("Availability", back_populates="employee")

    def __init__(self, fname: str, lname: str, av: list[Availability], maximum:dict[int, int], min_hours: int, wage: float, level: int, tasks: list[int], location: str) -> None:
        self.fname = fname
        self.lname = lname
        self.name = f'{fname} {lname}'
        self.id: int = None
        self.availability = self.sort_availability(av)
        self.wage = wage
        self.weekly_max = maximum
        self.min_hours = min_hours
        self.level = level
        self.tasks = tasks
        self.location = location # where does this employee work? coffecompany, bagels and beans or google?
        self.availability = self.sort_availability(av)

    def sort_availability(self, av):
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

    def get_av(self) -> list[Availability]:
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
    