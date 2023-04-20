from datetime import datetime
from dataclasses import dataclass

@dataclass
class Availability:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        self.duration = (self.end - self.start).total_seconds() / 3600

    def __str__(self) -> str:
        start_time = self.start.strftime("%m-%d %H:%M")
        end_time = self.end.strftime("%m-%d %H:%M")
        return f"{start_time} - {end_time}"