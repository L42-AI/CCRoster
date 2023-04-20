

from classes.representation.employee import Employee
from classes.representation.shift import Shift
from classes.representation.availability import Availability
from classes.representation.shift_constraints import ShiftConstrains
from classes.representation.workload import Workload

from data.assign import shift_list, employee_list

class Availabilities:

    def __init__(self) -> None:

        self.total = {shift.id: self.get_employee_set(shift) for shift in shift_list}
        self.actual = {shift_id: [0, availabilities_set] for shift_id, availabilities_set in self.total.items()}

        self.update_highest_priority_list()

    """ INIT """

    def get_employee_set(self, shift: Shift) -> set[int]:
        """
        this method is only used to develop the generator, later, the info will actually be downloaded
        for now it just returns a hardcoded list with availability
        """

        availabilities = set()
        for employee in employee_list:

            for weeknum in employee.availability:
                for workable_shift in employee.availability[weeknum]:

                    if self.possible_shift(workable_shift, employee, shift):
                        availabilities.add(employee.id)

        return availabilities
    
    def set_shift_occupation(self, shift_id: int, occupied: bool) -> None:
        if occupied:
            self.actual[shift_id][0] = 1
        else:
            self.actual[shift_id][0] = 0

    """ METHODS """

    def update_availabilty(self, shift_constrains: ShiftConstrains, shift_id: int, employee_id: int, add: bool, max_hit: bool = False) -> None:

        self.set_shift_occupation(shift_id, add)

        coliding_shifts = shift_constrains[shift_id]

        if add:
            for coliding_shift_id in coliding_shifts:
                if employee_id in self.actual[coliding_shift_id][1]:
                    self.actual[coliding_shift_id][1].remove(employee_id)

            if max_hit:
                for shift_id in self.actual:
                    if employee_id in self.actual[shift_id][1]:
                        self.actual[shift_id][1].remove(employee_id)
        else:
            for shift_id in self.actual:
                if employee_id in self.actual[shift_id][1]:
                    self.actual[shift_id][1].add(employee_id)
    
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
                # print(employee.name, employee.priority, week_min, week_max, len(self.workload[employee.id][weeknum]))
            else:
                employee.priority = 999
    
    def update_highest_priority_list(self) -> None:
        self.priority_list = sorted(
            employee_list, key=lambda employee: employee.priority)

    def possible_shift(self, workable_shift: Availability, employee: Employee, shift: Shift) -> bool:

        # Check time
        if workable_shift.start > shift.start or workable_shift.end < shift.end:
            return False

        # Check task
        tasks_list = employee.get_tasks()
        for task in tasks_list:
            if task == shift.task:
                return True
        return False