import random

from model.representation.data_classes.shift import Shift
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.availability import Availability


def gen_id_dict(list: list) -> dict[int, object]:
    return {x.id : x for x in list}

def gen_time_conflict_dict(shift_list: list[Shift]) -> dict[int, set[int]]:
    time_conflict_dict = {shift.id: set() for shift in shift_list}
    for i, shift_1 in enumerate(shift_list):

        for shift_2 in shift_list[i+1:]:
            if shift_1.end < shift_2.start:
                continue
            if shift_1.start < shift_2.end:
                time_conflict_dict[shift_1.id].add(shift_2.id)
                time_conflict_dict[shift_2.id].add(shift_1.id)

    return time_conflict_dict

def get_standard_cost(employee_list: list[Employee]) -> float:
    total = sum([employee.get_minimal_hours() * employee.get_wage()  for employee in employee_list])
    return round(total, 2)

def get_random_shift(shift_list: list[Shift]) -> int:
    return random.choice(shift_list).id

def get_random_employee(total_availabilities: dict, shift_id: int, existing_employee: int = None) -> int:
    """
    returns an employee id
    """

    if existing_employee != None:
        choices = total_availabilities[shift_id] - {existing_employee}
    else:
        choices = total_availabilities[shift_id]
    
    if not choices:
        raise ValueError("No available employees for shift")

    return random.choice(list(choices))

def recursive_copy(obj: object) -> object:

    if isinstance(obj, dict):
        return {k: recursive_copy(v) for k, v in obj.items()}

    elif isinstance(obj, set):
        return {recursive_copy(x) for x in obj}

    elif isinstance(obj, list):
        return [recursive_copy(x) for x in obj]
    
    else:
        # final return
        return obj



def _possible_shift(workable_shift: Availability, employee: Employee, shift: Shift) -> bool:

    # Check time
    if workable_shift.start > shift.start or workable_shift.end < shift.end:
        return False

    # Check task
    tasks_list = employee.get_tasks()
    for task in tasks_list:
        if task == shift.task:
            return True
    return False

def _employee_availability(shift: Shift, employee_list: list[Employee]) -> set[int]:
    """
    this method is only used to develop the generator, later, the info will actually be downloaded
    for now it just returns a hardcoded list with availability
    """

    availabilities = set()
    for employee in employee_list:
        for weeknum in employee.availability_dict:
            for workable_shift in employee.availability_dict[weeknum]:

                if _possible_shift(workable_shift, employee, shift):
                    availabilities.add(employee.id)

    return availabilities

def gen_total_availabilities(employee_list: list[Employee], shift_list: list[Shift]):
    return {shift.id: _employee_availability(shift, employee_list) for shift in shift_list}