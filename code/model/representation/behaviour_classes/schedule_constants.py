from model.representation.data_classes.availability import Availability
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

def get_standard_cost(employee_list: list[Employee]) -> float:
    """
    calculates the total costs of a schedule
    """
    # calculate the starting costs
    total = sum([employee.get_minimal_hours() * employee.get_wage()  for employee in employee_list])

    return round(total, 2)

