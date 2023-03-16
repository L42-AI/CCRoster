from dataclasses import dataclass
from datetime import datetime

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

    def __str__(self) -> str:
        start_time = self.start.strftime("%m-%d %H:%M")
        end_time = self.end.strftime("%m-%d %H:%M")
        return f"Task {self.task} from {start_time} to {end_time}"