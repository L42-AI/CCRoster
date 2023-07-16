import datetime

from sqlalchemy import Column, Integer, DateTime
from model.representation.data_classes.setup import Base

class Shift(Base):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    location = Column(Integer)
    task = Column(Integer)

    def __init__(self, start: datetime.datetime, end: datetime.datetime, task: int, location: int) -> None:
        self.start = start
        self.end = end
        self.task = task
        self.location = location
        self.duration = (self.end - self.start).total_seconds() / 3600

    def __str__(self) -> str:
        start_time = self.start.strftime("%m-%d %H:%M")
        end_time = self.end.strftime("%m-%d %H:%M")
        return f"ID:{self.id}, Time: {start_time} - {end_time}, Task: {self.task}, Weeknum:{self.start.isocalendar()[1]}"
    
    def get_id(self) -> int:
        if self.id == -999:
            raise ValueError('No Valid ID assigned to shift')
        return self.id
    
    def to_dict(self) -> dict:
        return {'id': self.id, 'start': self.start, 'end': self.end, 'location': self.location}