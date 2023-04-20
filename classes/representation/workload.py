
from data.assign import employee_list
from classes.representation.employee import Employee

from helpers import get_weeknumber, get_employee

class Workload(dict):

    def __init__(self) -> None:
        super().__init__(self)

        self.init_workload(employee_list)

    """ INIT """

    def init_workload(self, employees: list[Employee]) -> dict[int, dict[int, list]]:
        for employee in employees:
            self[employee.id] = {weeknum: [] for weeknum in employee.availability}
    
    """"""

    """ METHODS """

    def check_capacity(self, shift_id: int, employee_id: int) -> bool:
        """
        returns True if the employee is allowed to work that shift given his/hers weekly max
        """

        employee_obj = get_employee(employee_id)

        # get the week and check how many shifts the person is working that week
        weeknumber = get_weeknumber(shift_id)

        if employee_obj.get_week_max(weeknumber) > (len(self[employee_id][weeknumber])):
            return True
        else:
            # if the person will not take on the shift, delete it from the workload
            return False

    def update(self, shift_id: int, employee_id: int, add=False) -> None:
        """
        updates workload dictionary when an employee takes on a new shift
        """
        # get the week number of the shift
        weeknumber = get_weeknumber(shift_id)

        if weeknumber not in self[employee_id]:
            self[employee_id] = {weeknumber: []}

        if add:
            # add a shift to the workload of that employee that week
            self[employee_id][weeknumber].append(shift_id)
        else:
            self[employee_id][weeknumber].remove(shift_id)