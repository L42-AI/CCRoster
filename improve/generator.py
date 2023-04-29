import random
import copy
import math
from representation.shift_constraints import ShiftConstrains
from representation.malus_calc import MalusCalc
from representation.workload import Workload
from representation.schedule import Schedule

from helpers import recursive_copy, id_employee, id_shift
from data.assign import employee_list, shift_list
from data.schedule_constants import total_availabilities

OFFLINE = True  # employee.id is downloaded from the server, so when offline, use index of employee object in employeelist as id

class Generator:
    def __init__(self) -> None:
        self.shifts = shift_list  # shift list from assign with shift instances
        self.employees = employee_list
        self.id_employee = id_employee
        self.id_shift = id_shift

        self.ShiftConstrains = ShiftConstrains()
        self.Workload = Workload()
        self.standard_cost = MalusCalc.standard_cost(self.employees)

        self.Schedule = Schedule(self.Workload, 999999, None)

    """ Schedule manipulation """

    def schedule_in(self, shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        ''' Places a worker in a shift in the schedule, while also updating his workload '''
        Schedule[shift_id] = employee_id
        Schedule.Workload.update(shift_id, employee_id, add=True)

    def schedule_out(self, shift_id: int, Schedule: Schedule) -> None:
        ''' Removes a worker from a shift and updates the workload so the worker has room to work another shift'''
        employee_id = Schedule[shift_id]
        Schedule[shift_id] = None
        Schedule.Workload.update(shift_id, employee_id, add=False)

    def schedule_swap(self, shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        ''' Performs a swap in workers for a shift, updates the workload of both workers in the process'''
        self.schedule_out(shift_id, Schedule)
        self.schedule_in(shift_id, employee_id, Schedule)

    """ MUTATE """

    def mutate(self, schedule: Schedule, T: float) -> list[Schedule]:
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # buds will be the mutated schedules
        buds = []
        old_cost = MalusCalc.compute_cost(self.standard_cost, schedule)
        while len(buds) < 10:
            
            # copy the original schedule
            bud_schedule = Schedule(Workload(recursive_copy(schedule.Workload)), old_cost, recursive_copy(schedule))
            for _ in range(schedule.MUTATIONS):
                buds = self.modification(buds, bud_schedule, T)
        return buds
    
    def modification(self, buds, schedule: Schedule, T) -> Schedule:
        # find a modification            
        replace_shift_id = self.get_random_shift()
        current_employee_id = schedule[replace_shift_id]
        replace_employee_id = self.get_random_employee(replace_shift_id, current_employee_id, schedule)
        old_cost = schedule.cost

        # check if new worker wants to work additional shift, if not, use mutate_max
        if schedule.Workload.check_capacity(replace_shift_id, replace_employee_id):

            if ShiftConstrains.passed_hard_constraints(replace_shift_id, replace_employee_id, schedule):
                self.schedule_swap(replace_shift_id, replace_employee_id, schedule)
                buds = self.accept_change(schedule, old_cost, buds, T, shift_id=replace_shift_id, new_emp=replace_employee_id, old_emp=current_employee_id, skip_shift_id=replace_shift_id)            
                
            return buds
        else: # if worker does not want an additional shift, have someone else work on of the worker's shift
            schedule = self.mutate_max_workload(replace_shift_id, replace_employee_id, schedule) 
            buds = self.accept_change(schedule, old_cost, buds, T, skip_shift_id=replace_shift_id, )
            return buds
        
    def accept_change(self, bud_schedule: Schedule, old_cost: int, buds: list, T: float, shift_id: int=None, new_emp: int=None, old_emp: int=None, skip_shift_id=None) -> list:
        ''' Method that evaluates if a mutated schedule will be accepted based on the new cost
            and a simulated annealing probability'''
        if shift_id != None: # does not take into account 'free' hours
        #     # print(sum([self.id_shift[id_].duration for x in bud_schedule.Workload[new_emp] for id_ in bud_schedule.Workload[new_emp][x] if id_ != shift_id]), bud_schedule.Workload[new_emp][5])
        
            duration_old_emp, duration_new_emp = self.billable_hours(shift_id, old_emp, new_emp, bud_schedule)
            old_wage = self.id_employee[old_emp].wage
            new_wage = self.id_employee[new_emp].wage
            cost_old_emp = old_wage * duration_old_emp
            cost_new_emp = new_wage * duration_new_emp

            # print(old_cost - MalusCalc.compute_final_costs(self.standard_cost, bud_schedule), cost_old_emp - cost_new_emp)
            bud_schedule.cost = old_cost - cost_old_emp + cost_new_emp

        else:
            bud_schedule.cost = MalusCalc.compute_cost(self.standard_cost, bud_schedule)
        
        # store the costs in bud_schedule

        new_cost = bud_schedule.cost

        # if cost lower, do not make math calculation
        if new_cost < old_cost:
            buds.append(bud_schedule)
            return buds
        
        # accept only if it satisfies sim an condition
        exponent = -(new_cost - old_cost) / T
        exponent = max(-700, min(exponent, 700))
        p_acceptance = math.exp(exponent)
        if p_acceptance > random.random(): 
            buds.append(bud_schedule)
            
        return buds

    def mutate_max_workload(self, shift_to_replace_id: int, possible_employee_id: int, schedule: Schedule) -> list[tuple[int, int]]:
        '''
        Method gets called when mutate wants to schedule a worker for a shift but the worker is already
        working his/hers max. This method will replace one of his/her shifts to check if that will be cheaper
        '''

        # get the shortest shift the busy person is working
        shortest_shift_id = sorted(self.shifts, key=lambda x: x.duration)[0].id

        # make sure we do not get stuck in recursive loop
        if shift_to_replace_id == shortest_shift_id:
            return schedule

        # pick new employee to work the shortest shift
        shortest_shift_employee_id = self.get_random_employee(shortest_shift_id, possible_employee_id, schedule)

        # check if worker that will take over the shift, still wants to work additional shift
        if schedule.Workload.check_capacity(shortest_shift_id, shortest_shift_employee_id):
            if ShiftConstrains.passed_hard_constraints(shortest_shift_id, shortest_shift_employee_id, schedule):

                self.schedule_swap(shortest_shift_id, shortest_shift_employee_id, schedule)

        # find replacement for the replacement worker
        else: 
            self.mutate_max_workload(shortest_shift_id, shortest_shift_employee_id, schedule)
        return schedule

    """ Helper methods """
    def billable_hours(self, shift_id, old_emp, new_emp, bud_schedule):
            duration = self.id_shift[shift_id].duration
            duration_old_emp = max(0, duration - max(0, self.id_employee[old_emp].min_hours - sum([self.id_shift[id_].duration for x in bud_schedule.Workload[old_emp] for id_ in bud_schedule.Workload[old_emp][x]])))
            duration_new_emp = max(0, duration - max(0, self.id_employee[new_emp].min_hours - sum([self.id_shift[id_].duration for x in bud_schedule.Workload[new_emp] for id_ in bud_schedule.Workload[new_emp][x] if id_ != shift_id])))
            return duration_old_emp, duration_new_emp

    def get_random_shift(self) -> int:
        """
        returns a tuple with inside (1) a tuple containing shift info and (2) an index
        """

        shift_id = random.choice(self.shifts).id
        while len(total_availabilities[shift_id]) < 2:
            shift_id = random.choice(self.shifts).id
        return shift_id

    def get_random_employee(self, shift_id: int, current_employee_id: int, schedule: Schedule) -> int:
        """
        returns an employee id
        """

        # see who is working already to avoid duplicate
        current_employee_id = schedule[shift_id]

        choices = total_availabilities[shift_id] - {current_employee_id}
        if not choices:
            raise ValueError("No available employees for shift")
        return random.choice(list(choices))

    def print_schedule(self, schedule: Schedule) -> None:
        # Format and print the schedule
        for shift_id, employee_id in schedule.items():
            print(id_shift[shift_id], id_employee[employee_id])
