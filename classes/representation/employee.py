import random
from datetime import datetime
from classes.representation.dataclasses import Availability
import uuid

class Employee:
    def __init__(self, fname, lname, av, maximum, minimum, wage, level, tasks, location) -> None:
        self.fname = fname
        self.lname = lname
        self.name = f'{fname} {lname}'
        self.id = None
        self.availability = av
        self.wage = wage
        self.weekly_max = maximum
        self.weekly_min = minimum
        self.level = level
        self.tasks = tasks
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

    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id})"

