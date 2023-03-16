from dataclasses import dataclass
from datetime import datetime

@dataclass
<<<<<<< HEAD
class Availability:
    start: datetime
    end: datetime

@dataclass
=======
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
class Shift:
    start: datetime
    end: datetime
    task: int
<<<<<<< HEAD
    location: int
=======
    location: int

@dataclass
class Availability:
    start: datetime
    end: datetime
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
