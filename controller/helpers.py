from controller.database import download_employees, download_shifts
# or
from controller.app import employee_list, shift_list 

''' When should helpers be created? maybe only after the login? than we can
    get id from current_user in app. it is only used in generator so when
    browsing we do not need to create this file. But should app hold those lists globally?
    currently only made inside functions. Maybe make class from app so the lists
    can be made attributes''' 
# id_employee = {employee.id: employee for employee in employee_list}
# id_shift = {shift.id: shift for shift in shift_list}

# def get_weeknumber(shift_id: int) -> int:
#     shift_obj = id_shift[shift_id]
#     return shift_obj.start.isocalendar()[1]

# def recursive_copy(obj: object) -> object:

#     if isinstance(obj, dict):
#         return {k: recursive_copy(v) for k, v in obj.items()}

#     elif isinstance(obj, set):
#         return {recursive_copy(x) for x in obj}

#     elif isinstance(obj, list):
#         return [recursive_copy(x) for x in obj]
    
#     else:
#         # final return
#         return obj