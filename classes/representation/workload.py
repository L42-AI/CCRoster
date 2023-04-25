
from data.assign import employee_list
from classes.representation.employee import Employee

from helpers import get_weeknumber, id_employee

class Workload(dict):

    def __init__(self, set_workload=None) -> None:
        super().__init__(self)

        if set_workload is not None:
            self.copy_workload(set_workload)
        else:
            self.init_workload(employee_list)

        self.update_highest_priority_list()

    """ INIT """

    def copy_workload(self, set_workload: dict[int, dict[int, list]]) -> None:
        for employee_id in set_workload:
            self[employee_id] = set_workload[employee_id]

    def init_workload(self, employee_list: list[Employee]) -> None:
        for employee in employee_list:
            self[employee.id] = {weeknum: [] for weeknum in employee.availability}

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

    def compute_priority(self, weeknum: int) -> None:
        for employee in employee_list:
            week_max = employee.get_week_max(weeknum)
            week_min = employee.get_week_min(weeknum)

            if weeknum in employee.availability:
                availability_priority = (
                    len(employee.availability[weeknum]) - week_max)
                week_min_priority = (len(self[employee.id][weeknum]) - week_min)
                week_max_priority = (week_max - len(self[employee.id][weeknum]))

                if availability_priority < 1:
                    availability_priority = -99
                if week_min_priority < 0:
                    week_min_priority = -150
                if week_max_priority < 1:
                    week_max_priority = -99

                employee.priority = availability_priority + \
                    week_min_priority - week_max_priority
            else:
                employee.priority = 999
    
    def update_highest_priority_list(self) -> None:
        self.priority_list = sorted(
            employee_list, key=lambda employee: employee.priority)