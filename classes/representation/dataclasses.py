from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Availability:
    start: datetime
    end: datetime

@dataclass
class Shift:
    start: datetime
    end: datetime
    task: int
    location: int

    def __post_init__(self) -> None:
        self.duration = (self.end - self.start).total_seconds() / 3600
        self.id = str(uuid.uuid4())

    def __str__(self) -> str:
        start_time = self.start.strftime("%m-%d %H:%M")
        end_time = self.end.strftime("%m-%d %H:%M")
        return f"Task {self.task}, {start_time} - {end_time}"
    
    def get_id(self) -> str:
        return self.id