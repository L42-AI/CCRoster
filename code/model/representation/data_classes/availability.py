from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from model.representation.data_classes.setup import Base

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
