

from representation.employee import Employee
from representation.shift import Shift
from representation.availability import Availability
from representation.shift_constraints import ShiftConstrains
from representation.workload import Workload

from data.schedule_constants import total_availabilities

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