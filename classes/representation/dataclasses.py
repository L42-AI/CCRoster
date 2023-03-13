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