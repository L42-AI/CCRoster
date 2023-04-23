from classes.representation.shift import Shift
from classes.representation.employee import Employee


from data.assign import employee_list, shift_list

id_employee = {employee.id: employee for employee in employee_list}
id_shift = {shift.id: shift for shift in shift_list}

def get_shift(id: int) -> Shift:
    return id_shift.get(id)

def get_employee(id: int) -> Employee:
    return id_employee.get(id)

def get_weeknumber(shift_id: int) -> int:
    shift_obj = get_shift(shift_id)
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

def get_temperature(T):
    return T*0.95