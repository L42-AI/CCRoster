from data.assign import employee_list
import random

class Switch:

    def random(schedule) -> list:
        random_week = random.randint(0, schedule.shape[0] - 1)
        random_day = random.randint(0, schedule.shape[1] - 1)
        random_shift = random.randint(0, schedule.shape[2] - 1)

        code = [random_week, random_day, random_shift]

        shift = schedule[random_week, random_day, random_shift]
        selected_employee = random.choice(shift)
        selected_employee_index = shift.index(selected_employee)

        new_employee = random.choice([emp for emp in employee_list if code in emp.availability and emp != selected_employee])
        schedule[random_week, random_day, random_shift][selected_employee_index] = f'!!!{new_employee.get_name()}!!!'

        return selected_employee_index, selected_employee, new_employee
