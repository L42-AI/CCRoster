from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model.representation.data_objects import Base, Employee

connection_string = 'mysql+mysqlconnector://Jacob:wouterisdebestehuisgenoot@185.224.91.162:3308/rooster'    
    
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
session = Session(engine)


def download_employees(id):
    print(id)
    employees = session.query(Employee).filter(Employee.location == id).all()
    print(employees)

