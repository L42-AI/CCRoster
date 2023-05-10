from model.representation.employee import Employee

from data.assign import employee_list
from helpers import get_weeknumber, id_employee

class Workload(dict):

    def __init__(self, set_workload=None) -> None:
        super().__init__(self)

        if set_workload is not None:
            self.copy_workload(set_workload)
        else:
            self.init_workload(employee_list)

    """ INIT """

    def copy_workload(self, set_workload: dict[int, dict[int, list]]) -> None:
        for employee_id in set_workload:
            self[employee_id] = set_workload[employee_id]

    def init_workload(self, employee_list: list[Employee]) -> None:
        for employee in employee_list:
            self[employee.id] = {weeknum: [] for weeknum in employee.weekly_max}

    """ METHODS """

    def check_capacity(self, shift_id: int, employee_id: int) -> bool:
        """
        returns True if the employee is allowed to work that shift given his/hers weekly max
        """

        employee_obj = id_employee[employee_id]

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
        elif employee_id != 10: # hardcoded for dummy employee!! remove after testing
            self[employee_id][weeknumber].remove(shift_id)