import random

from classes.representation.dataclasses import Shift, Availability
from classes.representation.employee import Employee

class Greedy:
    def fill_employees(schedule: list[tuple[int, None]], employee_list:list[Employee]) -> list[tuple[int,int]]:
        # Sort on availability to first do people with little availability
        sorted_employees = sorted(employee_list, key=lambda employee: len(employee.availability))

        added = 0

        while added < len(schedule):
            for i, employee in enumerate(sorted_employees):
                schedule[i] = (schedule[i][0], employee.get_id())
                added += 1
        return schedule

    def fill_shifts(schedule: list[tuple[int, None]], shift_list: list[Shift], availability_list: list[list[int]]) -> list[tuple[int,int]]:
        def get_random_employee(index) -> int:
            return random.choice(availability_list[index])
        
        indexes_list = [i for i in range(len(shift_list))]

        sorted_index = sorted(indexes_list, key = lambda i: len(availability_list[i]))

        for index in sorted_index:
            random_employee = get_random_employee(index)
            schedule[index] = (schedule[index][0], random_employee)
        
        return schedule
