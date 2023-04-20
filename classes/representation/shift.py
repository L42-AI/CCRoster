from datetime import datetime
from dataclasses import dataclass

@dataclass
class Shift:
    start: datetime
    end: datetime
    task: int
    location: int

    def __post_init__(self) -> None:
        self.id = -999
        self.duration = (self.end - self.start).total_seconds() / 3600

    def __str__(self) -> str:
        start_time = self.start.strftime("%m-%d %H:%M")
        end_time = self.end.strftime("%m-%d %H:%M")
        return f"Task {self.task}, {start_time} - {end_time}"
    
    def get_id(self) -> int:
        if self.id == -999:
            raise ValueError('No Valid ID assigned to shift')
        return self.id