import random
from datetime import datetime
from classes.representation.dataclasses import Availability

class Employee:
    def __init__(self, fname, lname, av, maximum, wage, level, task, location) -> None:
        self.fname = fname
        self.lname = lname
        self.name= fname + " " + lname
        self.id: int = None
        self.availability = av
        self.wage = wage
        self.weekly_max = maximum
        self.level = level
        self.tasks = 1 if task=='everything' else 0
        self.location = location # where does this employee work? coffecompany, bagels and beans or google?
        self.add_remove_timeslot = []

        # self.upload_employee()
        # self.upload_availability()

    """ Get """
    def get_name(self):
        return self.name

    def get_full_av(self) -> set:
        return self.availability

    def get_av(self) -> list[int]:
        if len(self.availability) > 0:
            return random.choice(self.availability)

    def get_name(self, name) -> str:
        return name

    def get_wage(self) -> float:
        return float(self.wage)

    def get_level(self) -> int:
        return self.level

    def get_tasks(self) -> int:
        return self.tasks

    def get_week_max_dict(self) -> dict:
        return self.weekly_max

    def get_week_max(self, week) -> int:
        return self.weekly_max.get(week)

    def get_id(self) -> int:
        return self.id

