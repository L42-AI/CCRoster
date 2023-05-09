from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
# from controller.helpers import get_weeknumber, id_employee
import random

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(100))
    last_name = Column(VARCHAR(100))
    wage = Column(Float)
    min_hours = Column(Integer)
    level = Column(Integer)
    location = Column(String)
    
    availability = relationship("Availability", back_populates="employee", cascade="all, delete, delete-orphan")
    weekly_maxs = relationship("Weekly_max", back_populates="employee")
    task = relationship("Task", back_populates="employee")

    def __init__(self, first_name: str, last_name: str, availability, maximum:dict[int, int], min_hours: int, wage: float, level: int, tasks: list[int], location: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.availability = availability
        self.wage = wage
        self.weekly_max = maximum
        self.min_hours = min_hours
        self.level = level
        self.tasks = tasks
        self.location = location

    
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
    
class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    employee = relationship("Employee", back_populates="availability")

    def __init__(self, start: datetime, end: datetime):
        self.employee_id = None
        self.start = start
        self.end = end
        self.duration = (self.end - self.start).total_seconds() / 3600

    def __str__(self) -> str:
        start_time = self.start.strftime("%m-%d %H:%M")
        end_time = self.end.strftime("%m-%d %H:%M")
        return f"{start_time} - {end_time}"


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


class Shift(Base):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    location = Column(Integer)
    task = Column(Integer)

    def __init__(self, start, end, task, location) -> None:
        self.start = start
        self.end = end
        self.task = task
        self.location = location
        self.duration = (self.end - self.start).total_seconds() / 3600

    def __str__(self) -> str:
        start_time = self.start.strftime("%m-%d %H:%M")
        end_time = self.end.strftime("%m-%d %H:%M")
        return f"Task {self.task}, {start_time} - {end_time}"
    
    def get_id(self) -> int:
        if self.id == -999:
            raise ValueError('No Valid ID assigned to shift')
        return self.id
    

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    task= Column(Integer)

    employee = relationship("Employee", back_populates="task")

class Workload(dict):

    def __init__(self, set_workload=None) -> None:
        super().__init__(self)

        if set_workload is not None:
            self.copy_workload(set_workload)
        else:
            self.init_workload(employee_list)

    """ INIT """

    def copy_workload(self, set_workload: dict[int, dict[int, list]]) -> None:
        for employee_id in set_workload:
            self[employee_id] = set_workload[employee_id]

    def init_workload(self, employee_list: list[Employee]) -> None:
        for employee in employee_list:
            self[employee.id] = {weeknum: [] for weeknum in employee.availability}

    """ METHODS """

    def check_capacity(self, shift_id: int, employee_id: int) -> bool:
        """
        returns True if the employee is allowed to work that shift given his/hers weekly max
        """

        employee_obj = id_employee[employee_id]

        # get the week and check how many shifts the person is working that week
        weeknumber = get_weeknumber(shift_id)

        if employee_obj.get_week_max(weeknumber) > (len(self[employee_id][weeknumber])):
            return True
        else:
            # if the person will not take on the shift, delete it from the workload
            return False

    def update(self, shift_id: int, employee_id: int, add=False) -> None:
        """
        updates workload dictionary when an employee takes on a new shift
        """
        # get the week number of the shift
        weeknumber = get_weeknumber(shift_id)

        if weeknumber not in self[employee_id]:
            self[employee_id] = {weeknumber: []}

        if add:
            # add a shift to the workload of that employee that week
            self[employee_id][weeknumber].append(shift_id)
        elif employee_id != 10: # hardcoded for dummy employee!! remove after testing
            self[employee_id][weeknumber].remove(shift_id)

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.now())  # Timestamp of when the schedule was created

    def __init__(self, Workload: Workload, cost: float, shift_list, set_schedule: dict[int, int] = None):
        self.Workload = Workload
        self.cost = cost

        self.fitness: float = None
        self.p: float = None
        self.BUDS = 10 # number of buds this plant can have
        self.MUTATIONS = random.randint(1, 5)

        if set_schedule is not None:
            for shift_id in set_schedule:
                self[shift_id] = set_schedule[shift_id]
        else:
            for shift in shift_list:
                self[shift.id] = 10 #HARDCODED DUMMY EMPL