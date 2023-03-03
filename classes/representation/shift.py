from dataclasses import dataclass

@dataclass
class Shift:
    start_time: str
    end_time: str
    day: int
    week: int
    role: int
    location: int
