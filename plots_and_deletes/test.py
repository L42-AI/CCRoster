import random

from classes.representation.shift_constraints import ShiftConstrains
from classes.representation.availabilities import Availabilities
from classes.representation.workload import Workload


from helpers import get_weeknumber, id_employee
from data.assign import shift_list

class Schedule(dict):
    def __init__(self):
        super().__init__(self)

        for shift in shift_list:
            self[shift.id] = None
        
    def random_fill(self) -> None:

        filled = 0
        while filled < len(self):
            shift_id = random.choice(self)

            if self[shift_id] != None:
                continue

            selected_employee = random.choice(self)
            self.schedule_in(shift_id, selected_employee.id)

            filled += 1

    def greedy_fill(self, Availabilities: Availabilities, Workload: Workload, ShiftConstrains: ShiftConstrains) -> None:

        filled = 0
        while filled < len(self):

            sorted_id_list = sorted(self.keys(), key = lambda shift_id: len(Availabilities.actual[shift_id][1]) if Availabilities.actual[shift_id][0] == 0 else 999)

            for shift_id in sorted_id_list:
                if self[shift_id] != None:
                    continue
                # if len(self.actual_availabilities[sorted_id_list[0]][1]) < 2:
                #     shift_id = sorted_id_list[0]
                elif len(Availabilities.actual[shift_id][1]) < 1:
                    raise LookupError('No availabilities for shift!')

                weeknum = get_weeknumber(shift_id)

                Availabilities.compute_priority(Workload, weeknum)
                Availabilities.update_highest_priority_list()

                possible_employee_list = list(Availabilities.actual[shift_id][1])
                selected_employee_id = random.choice(possible_employee_list)
                
                for employee_id in possible_employee_list:
                    if id_employee[employee_id].priority < get_employee(selected_employee_id).priority:
                        selected_employee_id = employee_id
                
                if ShiftConstrains.passed_hard_constraints(shift_id, selected_employee_id, self):
                    self.schedule_in(Workload, Availabilities, ShiftConstrains, shift_id, selected_employee_id, fill=True)
                    filled += 1

    def schedule_in(self, Workload: Workload, Availabilities: Availabilities, ShiftConstrains: ShiftConstrains, shift_id: int, employee_id: int, fill: bool = False) -> None:
        self[shift_id] = employee_id
        Workload.update(shift_id, employee_id, add=True)

        if fill:
            week_num = get_weeknumber(shift_id)
            employee_obj = get_employee(employee_id)
            emlployee_week_max = employee_obj.get_week_max(week_num)

            if len(Workload[employee_id][week_num]) == emlployee_week_max:
                Availabilities.update_availabilty(ShiftConstrains, shift_id, employee_id, add=True, max_hit=True)
            else:
                Availabilities.update_availabilty(ShiftConstrains, shift_id, employee_id, add=True, max_hit=False)

    def schedule_out(self, Workload: Workload, Availabilities: Availabilities, ShiftConstrains: ShiftConstrains, shift_id: int, fill: bool = False) -> None:
        employee_id = self[shift_id]
        self[shift_id] = None
        Workload.update(shift_id, employee_id, add=False)
        
        if fill:
            Availabilities.update_availabilty(ShiftConstrains, shift_id, employee_id, add=False)

    def schedule_swap(self, shift_id: int, employee_id: int) -> None:
        self.schedule_out(shift_id)
        self.schedule_in(shift_id, employee_id)

    # def copy(self, schedule: Schedule) -> dict[int, int]:

    #     return {k: v for k, v in schedule.items()}
        
    def recursive_copy(self, obj: object) -> object:
        """
        This method that makes a copy of our schedule that does not change the schedule
        when we modify the copy. This eliminates the need for deepcopy
        """

        # if instance is a dict
        if isinstance(obj, dict):

            # return object comprehension with recursive function call
            return {k: self.recursive_copy(v) for k, v in obj.items()}

        # if instance is a set
        elif isinstance(obj, set):

            # return object comprehension with recursive function call
            return {self.recursive_copy(x) for x in obj}

        # if instance is a set
        elif isinstance(obj, list):

            # return object comprehension with recursive function call
            return {self.recursive_copy(x) for x in obj}
        
        else:
            # final return
            return obj