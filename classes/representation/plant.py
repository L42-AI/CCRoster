import random
from classes.representation.generator import Generator
from classes.representation.workload import Workload
from classes.representation.shift_constraints import ShiftConstrains
from classes.representation.availabilities import Availabilities
from classes.representation.malus_calc import MalusCalc

from data.assign import employee_list, shift_list, total_availabilities

class Plant(Generator):
    def __init__(self, P: int, schedule: dict[int, int], workload: Workload) -> None:
        super().__init__()
        self.sim_an = P # probability of accpeting worsening of cost
        self.schedule = schedule
        self.Workload = workload

        self.employees = employee_list
        self.employees = employee_list

        self.improve(200)

        self.total_costs = MalusCalc.get_total_cost(self.schedule, self.Workload)

        
    """ MUTATE """

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
                        
            # leave a bad change with probability of self.sim_an
            if MalusCalc.get_total_cost(self.schedule, self.Workload) > current_cost and random.random() > self.sim_an:

                self.schedule_swap(replace_shift_id, current_employee_id)
        
        else:

            # try to 'ease' workers workload by having someone else take over the shift, store the changes 
            undo_update = self.mutate_max_workload(replace_shift_id, replace_employee_id) 
           
            total_costs_new = MalusCalc.get_total_cost(self.schedule, self.Workload)

            # compare costs
            if total_costs_new > current_cost and random.random() > self.sim_an:

                for shift_id, employee_id in undo_update:
                    # swap back
                    self.schedule_swap(shift_id, employee_id)

        


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


   