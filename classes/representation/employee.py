import random

class Employee:
    def __init__(self, first_name, last_name, av, maximum, wage, onboarding, roles) -> None:
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.name: str = self.get_full_name(self.first_name, self.last_name)
        self.availability: list[list] = av
        self.weekly_max: dict = maximum
        self.wage: float = wage
        self.onboarding: int = onboarding
        self.roles: list[str] = roles

    """ Get """

    def get_full_av(self) -> set:
        return self.availability

    def get_av(self) -> list[int]:
        if len(self.availability) > 0:
            return random.choice(self.availability)

    def get_full_name(self, first_name, last_name) -> str:
        return f'{first_name}{last_name}'

    def get_abreviated_name(self) -> str:
        return f'{self.first_name[0]}. {self.last_name}'

    def get_wage(self) -> float:
        return float(self.wage)

    def get_onboarding(self) -> int:
        return self.onboarding

    def get_week_max_dict(self) -> dict:
        return self.weekly_max

    def get_week_max(self, week) -> int:
        return self.weekly_max.get(week)