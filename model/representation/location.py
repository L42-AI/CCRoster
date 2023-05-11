from sqlalchemy import Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

LOCATIONS = {
    1 : 'CoffeeCompany__NAME__'
}

class Location(Base):
    """
    Class representing location and name of location
    """
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100))

    def __init__(self, id_: int) -> None:
        self.id = id_
        self.name = LOCATIONS[self.id]

class HardContraint(Base):
    """
    Class representing each hard constrain function
    used for given location
    """
    __tablename__ = 'hard_constraints'

    location_id = Column(Integer, ForeignKey('location.id'))
    function_name = Column(VARCHAR(100))

    def __init__(self, location_id: int, function_name: str):
        self.location_id = location_id
        self.function_name = function_name
