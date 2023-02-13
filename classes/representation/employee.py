import random

class Employee:
    def __init__(self, name, av, maximum, wage, onboarding) -> None:
        self.name = name
        self.availability = av
        self.wage = wage
        self.weekly_max = maximum
        self.onboarding = onboarding

    """ Get """

    def get_av(self) -> list:
        if len(self.availability) > 0:
            return random.choice(self.availability)

    def get_name(self) -> str:
        return self.name

    def get_wage(self) -> float:
        return float(self.wage)

    def get_onboarding(self) -> bool:
        return self.onboarding

    def get_week_max_dict(self) -> dict:
        return self.weekly_max

    def get_week_max(self, week) -> int:
        return self.weekly_max.get(week)