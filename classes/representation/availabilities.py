

from classes.representation.employee import Employee
from classes.representation.shift import Shift
from classes.representation.availability import Availability
from classes.representation.shift_constraints import ShiftConstrains
from classes.representation.workload import Workload

from data.assign import employee_list, total_availabilities

class Availabilities(dict):

    def __init__(self, availabilities=None) -> None:
        super().__init__(self)

        if availabilities != None:
            prior_availabilities = availabilities
        else:
            prior_availabilities = total_availabilities
        
        for shift_id, availabilities_set in prior_availabilities.items():
            self[shift_id] =  [0, availabilities_set]

    """ INIT """
    
    def set_shift_occupation(self, shift_id: int, occupied: bool) -> None:
        if occupied:
            self[shift_id][0] = 1
        else:
            self[shift_id][0] = 0

    """ METHODS """

    def update_availabilty(self, shift_constrains: ShiftConstrains, shift_id: int, employee_id: int, add: bool, max_hit: bool = False) -> None:

        self.set_shift_occupation(shift_id, add)

        coliding_shifts = shift_constrains[shift_id]

        if add:
            for coliding_shift_id in coliding_shifts:
                if employee_id in self[coliding_shift_id][1]:
                    self[coliding_shift_id][1].remove(employee_id)

            if max_hit:
                for shift_id in self:
                    if employee_id in self[shift_id][1]:
                        self[shift_id][1].remove(employee_id)
        else:
            for shift_id in self:
                if employee_id in self[shift_id][1]:
                    self[shift_id][1].add(employee_id)
    
    def compute_priority(self, workload: Workload, weeknum: int) -> None:
        for employee in employee_list:
            week_max = employee.get_week_max(weeknum)
            week_min = employee.get_week_min(weeknum)

            if weeknum in employee.availability:
                availability_priority = (
                    len(employee.availability[weeknum]) - week_max)
                week_min_priority = (len(workload[employee.id][weeknum]) - week_min)
                week_max_priority = (week_max - len(workload[employee.id][weeknum]))

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