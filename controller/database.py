from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session
from model.representation.data_objects import Base, Employee, Shift
import datetime 

connection_string = 'mysql+mysqlconnector://Jacob:wouterisdebestehuisgenoot@185.224.91.162:3308/rooster'    
    
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
session = Session(engine)


def download_employees(id):
    employees = session.query(Employee).filter(Employee.location == id).all()
    return employees

def download_shifts(id):
    # Calculate the date range
    now = datetime.datetime.now()
    two_months_ago = now - datetime.timedelta(days=60)
    three_months_ahead = now + datetime.timedelta(days=90)

    # Query shifts within the date range and location
    shifts = session.query(Shift).filter(
        and_(
            Shift.location == id,
            Shift.start >= two_months_ago,
            Shift.start <= three_months_ahead
        )
    ).all()
    print(shifts)
    return shifts