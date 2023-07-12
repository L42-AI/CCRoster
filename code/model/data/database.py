from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_
from sqlalchemy.ext.declarative import declarative_base

from model.representation.data_classes.shift import Shift
from model.representation.data_classes.employee import Employee, Weekly_max, Task

database_url = 'mysql+mysqlconnector://Jacob:wouterisdebestehuisgenoot@185.224.91.162:3308/rooster'


Base = declarative_base()
engine = create_engine(database_url)
Base.metadata.create_all(engine)

session = Session(engine)

def download_employees(location_id: int) -> list[Employee]:
    employees = session.query(Employee).filter(Employee.location == location_id).all()
    return employees

def download_shifts(location_id: int) -> list[Shift]:
    # Calculate the date range
    now = datetime.now()
    two_months_ago = now - timedelta(days=60)
    three_months_ahead = now + timedelta(days=90)

    # Query shifts within the date range and location
    shifts = session.query(Shift).filter(
        and_(
            Shift.location == location_id,
            Shift.start >= two_months_ago,
            Shift.start <= three_months_ahead
        )
    ).all()
    print(shifts)
    return shifts

def create_employee_availability(employee):
    for av in employee.availability:
        session.add(av)

def create_employee_weekly_max(employee):
    for week, max_shifts in employee.weekly_max.items():
        wm = Weekly_max(week=week, max=max_shifts)
        wm.employee = employee
        session.add(wm)

def create_employee_tasks(employee):
    for task in employee.tasks:
        tsk = Task(employee_id=employee.id, task=task)
        session.add(tsk)

def upload(shift_list: list[Shift], employee_list: list[Employee]) -> None:
    """
    Uploads shifts and employees in the database.
    """

    for emp in employee_list:
        session.add(emp)
        create_employee_tasks(emp)
        create_employee_availability(emp)
        create_employee_weekly_max(emp)

    for shift in shift_list:
        session.add(shift)

    session.commit()
    session.close()

def download(location_id: int) -> tuple[list[Shift], list[Employee]]:
    employee_list = download_employees(location_id)
    shift_list = download_shifts(location_id)
    return shift_list, employee_list