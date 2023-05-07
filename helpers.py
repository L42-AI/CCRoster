from model.data.assign import employee_list, shift_list

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