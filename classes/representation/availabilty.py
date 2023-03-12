from dataclasses import dataclass
from datetime import date, time

@dataclass
class Availability:
    date: date
    start: time
    end: time