from classes.representation.employee import Employee
from classes.representation.shift import Shift

class Communicator:
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

    def create_employee(self, first_name, last_name, hourly_wage, level, roles):
        self.employee_list.append(
            Employee(
            first_name = first_name,
            last_name = last_name,
            av = [],
            maximum={},
            wage = hourly_wage,
            onboarding = level,
            roles = roles
            )
        )

    def edit_employee_availability(self, employee: Employee, availability_slot: list[int], add: bool):
        for employee_instance in self.employee_list:
            if employee_instance == employee:
                print(len(employee_instance.availability))

        if add:
            employee.availability.append(availability_slot)
        else:
            employee.availability.remove(availability_slot)

        for employee_instance in self.employee_list:
            if employee_instance == employee:
                print(len(employee_instance.availability))

    def delete_employee(self, first_name, last_name):
        for employee_instance in self.employee_list:
            if employee_instance.name == employee_instance.get_full_name(first_name, last_name):
                self.employee_list.remove(employee_instance)
                break

    def create_shift(self, time: str, day: str, week: str, role: str) -> None:
        start_time, end_time = self.get_start_and_finish_time(time)

        self.shift_list.append(
            Shift(
            start_time = start_time,
            end_time = end_time,
            day = day,
            week = week,
            role = role,
            location = self.location
            )
        )

    def delete_shift(self, time: str) -> None:
        self.to_delete: list[object] = []
        start_time, end_time = self.get_start_and_finish_time(time)

        for shift_instance in self.shift_list:
            if shift_instance.start_time == start_time and shift_instance.end_time == end_time:
                self.to_delete.append(shift_instance)

        for i in range(len(self.to_delete)):
            self.shift_list.remove(self.to_delete[i])