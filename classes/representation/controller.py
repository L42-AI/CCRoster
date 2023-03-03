
from classes.representation.employee import Employee
from classes.representation.shift import Shift

class Controller:
    def __init__(self, location) -> None:
        self.employee_list: list[Employee] = []
        self.shift_list: list[Shift] = []
        self.location = location

    """ Get """

    def get_employee_list(self) -> list:
        return self.employee_list

    def get_shift_list(self) -> list:
        return self.shift_list

    def get_start_and_finish_time(self, time: str) -> tuple:
        return time.split(' - ')

    def get_shift_info(self, info: dict) -> tuple:
        return info['day'], info['week'], info['type']

    """ Methods """

    def create_employee(self, *kwargs):
        print(kwargs)
        self.employee_list.append(
            Employee(
            )
        )

    def delete_employee(self, *kwargs):
        pass

    def create_shift(self, time: str, day: str, week: str, task: str) -> None:
        start_time, end_time = self.get_start_and_finish_time(time)

        self.shift_list.append(
            Shift(
            start_time = start_time,
            end_time = end_time,
            day = day,
            week = week,
            task = task,
            location = self.location
            )
        )

    def delete_shift(self, time: str) -> None:
        start_time, end_time = self.get_start_and_finish_time(time)

        for shift_instance in self.shift_list:
            if shift_instance.start_time == start_time and shift_instance.end_time == end_time:
                self.shift_list.remove(shift_instance)
