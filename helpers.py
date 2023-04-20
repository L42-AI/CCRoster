from classes.representation.shift import Shift
from classes.representation.employee import Employee


from data.assign import employee_list, shift_list


for id_, employee in enumerate(employee_list):
    employee.id_ = id_

for id_, shift in enumerate(shift_list):
    shift.id = id_

id_employee = {employee.id: employee for employee in employee_list}
id_shift = {shift.id: shift for shift in shift_list}

def get_shift(id: int) -> Shift:
    return id_shift.get(id)

def get_employee(id: int) -> Employee:
    return id_employee.get(id)

def get_weeknumber(shift_id: int) -> int:
    shift_obj = get_shift(shift_id)
    return shift_obj.start.isocalendar()[1]