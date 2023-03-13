from dataclasses import dataclass
import datetime

@dataclass
class Availability:
    start: datetime
    end: datetime