from sqlalchemy import Column, Integer, DateTime, VARCHAR

from model.representation.data_classes.setup import Base


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
    
    def db_to_instance(self):
        self.duration = (self.end - self.start).total_seconds() / 3600
    
    def get_id(self) -> int:
        if self.id == -999:
            raise ValueError('No Valid ID assigned to shift')
        return self.id
    
    def to_dict(self) -> dict:
        shift_dict = {'id': self.id, 'start': self.start, 'end': self.end, 'location': self.location, 'task': self.task}
        return shift_dict
    

