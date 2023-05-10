from model.representation.availability import Availability

class Employee:
    def __init__(self, fname: str, lname: str, av: list[Availability], maximum: dict[int, int], min_hours: int, wage: float, level: int, tasks: list[int], location: str) -> None:
        self.fname = fname
        self.lname = lname
        self.availability = self.sort_availability(av)
        self.weekly_max = maximum
        self.min_hours = min_hours
        self.wage = wage
        self.level = level
        self.tasks = tasks
        self.location = location # where does this employee work? coffecompany, bagels and beans or google?

        self.name = f'{fname} {lname}'
        self.id: int = None
        self.priority = 0

        # self.upload_employee()
        # self.upload_availability()

    """ Compute availability """

    def sort_availability(self, av: list[Availability]) -> dict[int, list[Availability]]:
        availability_dict = {}
        
        for availability in av:
            weeknum = availability.start.isocalendar()[1]

            if weeknum not in availability_dict:
                availability_dict[weeknum] = []

            availability_dict[weeknum].append(availability)
        return availability_dict

    """ Get """
    def get_name(self) -> str:
        return self.name

    def get_av(self) -> list[Availability]:
        return self.availability

    def get_wage(self) -> float:
        return float(self.wage)

    def get_level(self) -> int:
        return self.level

    def get_tasks(self) -> int:
        return self.tasks

    def get_week_max_dict(self) -> dict[int, int]:
        return self.weekly_max

    def get_week_max(self, week) -> int:
        return self.weekly_max.get(week)

    def get_minimal_hours(self) -> int:
        return self.min_hours

    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id})"
    