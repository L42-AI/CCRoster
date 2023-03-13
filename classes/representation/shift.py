
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
class ShiftData:
    start: time
    end: time
    task: int
    location: int