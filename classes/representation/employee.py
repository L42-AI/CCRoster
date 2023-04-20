from classes.representation.availability import Availability

class Employee:
    def __init__(self, fname: str, lname: str, av: list[Availability], maximum:dict[int, int], minimum: dict[int, int], wage: float, level: int, tasks: list[int], location: str) -> None:
        self.fname = fname
        self.lname = lname
        self.name = f'{fname} {lname}'
        self.id = None
        self.availability = self.sort_availability(av)
        self.wage = wage
        self.weekly_max = maximum
        self.weekly_min = minimum
        self.level = level
        self.tasks = tasks
        self.location = location # where does this employee work? coffecompany, bagels and beans or google?
        self.priority = 0
        self.add_remove_timeslot = []

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

    def get_week_min_dict(self) -> dict[int, int]:
        return self.weekly_min

    def get_week_min(self, week) -> int:
        return self.weekly_min.get(week)

    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id})"