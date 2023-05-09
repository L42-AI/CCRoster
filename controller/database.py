from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.representation.data_objects import Base

def connect_to_db():
    connection_string = 'mysql+mysqlconnector://Jacob:wouterisdebestehuisgenoot@185.224.91.162:3308/rooster'    
       
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session
session = connect_to_db()


