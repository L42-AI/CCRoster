from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from model.representation.data_objects import Employee, Shift, Weekly_max, Task
from assign import employee_list, shift_list

Base = declarative_base()
database_url = 'mysql+mysqlconnector://Jacob:wouterisdebestehuisgenoot@185.224.91.162:3308/rooster'

engine = create_engine(database_url)
Base.metadata.create_all(engine)

session = Session(engine)


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

def upload_assign(shift_list: list[Shift], employee_list: list[Employee]) -> None:
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
