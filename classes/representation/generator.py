import random

from classes.representation.shift_constraints import ShiftConstrains
from classes.representation.availabilities import Availabilities
from classes.representation.malus_calc import MalusCalc
from classes.representation.workload import Workload


from helpers import get_shift, get_employee, get_weeknumber
from data.assign import employee_list, shift_list, total_availabilities

OFFLINE = True  # employee.id is downloaded from the server, so when offline, use index of employee object in employeelist as id

class Generator:
    def __init__(self) -> None:
        self.shifts = shift_list  # shift list from assign with shift instances
        self.employees = employee_list

        self.ShiftConstrains = ShiftConstrains()
        self.Availabilities = Availabilities()
        self.Workload = Workload()

        self.schedule = {shift.id: None for shift in self.shifts}

        # self.improve(2000)

        # self.total_costs = MalusCalc.get_total_cost(self.schedule, self.Workload)
        # [print(f"Shift ID: {k}, available employee ID's: {v[1]}") for k, v in self.actual_availabilities.items()]

    """ Schedule manipulation """

    def random_fill(self) -> None:

        filled = 0
        while filled < len(self.schedule):
            shift_id = random.choice(self.schedule)

            if self.schedule[shift_id] != None:
                continue

            selected_employee = random.choice(self.schedule)
            self.schedule_in(shift_id, selected_employee.id)

            filled += 1

    def greedy_fill(self) -> None:

        filled = 0
        while filled < len(self.schedule):
            print(filled)
            sorted_id_list = sorted(self.schedule.keys(), key = lambda shift_id: len(self.Availabilities[shift_id][1]) if self.Availabilities[shift_id][0] == 0 else 999)

            for shift_id in sorted_id_list:
                if self.schedule[shift_id] != None:
                    continue
                # if len(self.actual_availabilities[sorted_id_list[0]][1]) < 2:
                #     shift_id = sorted_id_list[0]
                elif len(self.Availabilities[shift_id][1]) < 1:
                    raise LookupError('No availabilities for shift!')

                weeknum = get_weeknumber(shift_id)

                self.Workload.compute_priority(weeknum)
                self.Workload.update_highest_priority_list()

                possible_employee_list = list(self.Availabilities[shift_id][1])
                selected_employee_id = random.choice(possible_employee_list)
                
                for employee_id in possible_employee_list:
                    if get_employee(employee_id).priority < get_employee(selected_employee_id).priority:
                        selected_employee_id = employee_id
                
                if ShiftConstrains.passed_hard_constraints(shift_id, selected_employee_id, self.schedule):
                    self.schedule_in(shift_id, selected_employee_id, fill=True)
                    filled += 1

    def schedule_in(self, shift_id: int, employee_id: int, fill: bool = False) -> None:
        self.schedule[shift_id] = employee_id
        self.Workload.update(shift_id, employee_id, add=True)

        if fill:
            week_num = get_weeknumber(shift_id)
            employee_obj = get_employee(employee_id)
            emlployee_week_max = employee_obj.get_week_max(week_num)

            if len(self.Workload[employee_id][week_num]) == emlployee_week_max:
                self.Availabilities.update_availabilty(self.ShiftConstrains, shift_id, employee_id, add=True, max_hit=True)
            else:
                self.Availabilities.update_availabilty(self.ShiftConstrains, shift_id, employee_id, add=True, max_hit=False)

    def schedule_out(self, shift_id: int, fill: bool = False) -> None:
        employee_id = self.schedule[shift_id]
        self.schedule[shift_id] = None
        self.Workload.update(shift_id, employee_id, add=False)
        
        if fill:
            self.Availabilities.update_availabilty(self.ShiftConstrains, shift_id, employee_id, add=False)

    def schedule_swap(self, shift_id: int, employee_id: int) -> None:
        self.schedule_out(shift_id)
        self.schedule_in(shift_id, employee_id)

    """ MUTATE """

    def improve(self, iters: int) -> None:
        for _ in range(iters):
            self.mutate()
        print(MalusCalc.get_total_cost(self.schedule, self.Workload))

    def mutate(self):
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''
        replace_shift_id = self.get_random_shift()

        current_employee_id = self.schedule[replace_shift_id]
        replace_employee_id = self.get_random_employee(replace_shift_id, current_employee_id)

        current_cost = MalusCalc.get_total_cost(self.schedule, self.Workload)

        if self.Workload.check_capacity(replace_shift_id, replace_employee_id):

            if ShiftConstrains.passed_hard_constraints(replace_shift_id, replace_employee_id, self.schedule):
                # print('improvement')
                self.schedule_swap(replace_shift_id, replace_employee_id)
                        
            if MalusCalc.get_total_cost(self.schedule, self.Workload) > current_cost:

                self.schedule_swap(replace_shift_id, current_employee_id)
        
        else:

            # try to 'ease' workers workload by having someone else take over the shift, store the changes 
            undo_update = self.mutate_max_workload(replace_shift_id, replace_employee_id) 
           
            total_costs_new = MalusCalc.get_total_cost(self.schedule, self.Workload)

            # compare costs
            if total_costs_new > current_cost:

                for shift_id, employee_id in undo_update:
                    # swap back
                    self.schedule_swap(shift_id, employee_id)

        
    def mutate_extra_employees(self) -> None:
        sorted_shifts = sorted(self.schedule.keys(), key = lambda shift_id: self.actual_availabilities[shift_id][1], reverse=True)

        for shift_id in sorted_shifts:
            for employee_id in self.Availabilities.actual[shift_id][1]:
                if self.Workload.check_capacity(shift_id, employee_id):
                    ...
        return

    def mutate_max_workload(self, shift_to_replace_id: int, possible_employee_id: int) -> list[tuple[int, int]]:
        '''
        Method gets called when mutate wants to schedule a worker for a shift but the worker is already
        working his/hers max. This method will replace one of his/her shifts to check if that will be cheaper
        '''

        undo_update = []

        # get the shortest shift the busy person is working
        shortest_shift_id = sorted(self.shifts, key=lambda x: x.duration)[0].id

        if shift_to_replace_id == shortest_shift_id:
            return []

        # pick new employee to work the shortest shift
        shortest_shift_employee_id = self.get_random_employee(shortest_shift_id, possible_employee_id)

        if self.Workload.check_capacity(shortest_shift_id, shortest_shift_employee_id):
            if ShiftConstrains.passed_hard_constraints(shortest_shift_id, shortest_shift_employee_id, self.schedule):

                # store the changes ('old employee, shift')
                undo_update.append((shortest_shift_id, self.schedule[shortest_shift_id]))
                self.schedule_swap(shortest_shift_id, shortest_shift_employee_id)
        else:
            self.mutate_max_workload(shortest_shift_id, shortest_shift_employee_id)
        return undo_update

    """ Helper methods """

    def get_random_shift(self) -> int:
        """
        returns a tuple with inside (1) a tuple containing shift info and (2) an index
        """

        shift_id = random.choice(self.shifts).id
        while len(total_availabilities[shift_id]) < 2:
            shift_id = random.choice(self.shifts).id
        return shift_id

    def get_random_employee(self, shift_id: int, current_employee_id: int) -> int:
        """
        returns an employee id
        """
        current_employee_id = self.schedule[shift_id]

        choices = total_availabilities[shift_id] - {current_employee_id}
        if not choices:
            raise ValueError("No available employees for shift")
        return random.choice(list(choices))


    def print_schedule(self) -> None:
        # Format and print the schedule
        for shift_id, employee_id in self.schedule.items():
            print(get_shift(shift_id), get_employee(employee_id))
