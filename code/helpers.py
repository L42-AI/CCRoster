import random
from model.data.assign import employee_list, shift_list
from model.representation.behaviour_classes.schedule_constants import total_availabilities

id_employee = {employee.id: employee for employee in employee_list}
id_shift = {shift.id: shift for shift in shift_list}

def get_weeknumber(shift_id: int) -> int:
    shift_obj = id_shift[shift_id]
    return shift_obj.start.isocalendar()[1]

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

def get_random_shift() -> int:
    """
    returns a tuple with inside (1) a tuple containing shift info and (2) an index
    """

    shift_id = random.choice(shift_list).id
    while len(total_availabilities[shift_id]) < 2:
        shift_id = random.choice(shift_list).id
    return shift_id

def get_random_employee(shift_id: int, existing_employee: int = None) -> int:
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