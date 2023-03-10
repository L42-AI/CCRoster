from dataclasses import dataclass
from datetime import date, time

@dataclass
class Shift:
    start_time: str
    end_time: str
    day: int
    week: int
    task: int
    location: int

@dataclass
class Availability:
    day: date
    start: time
    end: time