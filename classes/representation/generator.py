import random
import copy
import math
import datetime

from classes.representation.shift_constraints import ShiftConstrains
from classes.representation.availabilities import Availabilities
from classes.representation.malus_calc import MalusCalc
from classes.representation.workload import Workload
from classes.representation.schedule import Schedule
from classes.representation.employee import Employee
from classes.representation.availability import Availability

from helpers import get_shift, get_employee, get_weeknumber, recursive_copy
from data.assign import employee_list, shift_list, total_availabilities

OFFLINE = True  # employee.id is downloaded from the server, so when offline, use index of employee object in employeelist as id

class Generator:
    def __init__(self) -> None:
        self.shifts = shift_list  # shift list from assign with shift instances
        self.employees = employee_list

        self.ShiftConstrains = ShiftConstrains()
        self.Availabilities = Availabilities()
        self.Workload = Workload()
        self.standard_cost = MalusCalc.standard_cost(self.employees)

        self.Schedule = Schedule(self.Workload, 999999, None)

    """ Schedule manipulation """

    def random_fill(self, Schedule) -> None:
        ''' yields terrible result, so it implies ppa still get stuck in local optima '''

        # fill with dummy employee
        for shift in self.shifts:
            self.schedule_in(shift.id, 10, Schedule)

    def greedy_fill(self) -> None:
        ''' Fills in the initial schedule in a greedy way '''

        filled = 0
        while filled < len(self.Schedule):
            sorted_id_list = sorted(self.Schedule.keys(), key = lambda shift_id: len(self.Availabilities[shift_id][1]) if self.Availabilities[shift_id][0] == 0 else 999)

            for shift_id in sorted_id_list:
                if self.Schedule[shift_id] != None:
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
                
                if ShiftConstrains.passed_hard_constraints(shift_id, selected_employee_id, self.Schedule):
                    self.schedule_in(shift_id, selected_employee_id, self.Schedule, fill=True)
                    filled += 1

    def schedule_in(self, shift_id: int, employee_id: int, Schedule: Schedule, fill: bool = False) -> None:
        ''' Places a worker in a shift in the schedule, while also updating his workload '''
        Schedule[shift_id] = employee_id
        Schedule.Workload.update(shift_id, employee_id, add=True)

        if fill:
            week_num = get_weeknumber(shift_id)
            employee_obj = get_employee(employee_id)
            employee_week_max = employee_obj.get_week_max(week_num)

            if len(Schedule.Workload[employee_id][week_num]) == employee_week_max:
                self.Availabilities.update_availabilty(self.ShiftConstrains, shift_id, employee_id, add=True, max_hit=True)
            else:
                self.Availabilities.update_availabilty(self.ShiftConstrains, shift_id, employee_id, add=True, max_hit=False)

    def schedule_out(self, shift_id: int, Schedule: Schedule, fill: bool = False) -> None:
        ''' Removes a worker from a shift and updates the workload so the worker has room to work another shift'''

        employee_id = Schedule[shift_id]
        Schedule[shift_id] = None
        Schedule.Workload.update(shift_id, employee_id, add=False)
        
        if fill:
            self.Availabilities.update_availabilty(self.ShiftConstrains, shift_id, employee_id, add=False)

    def schedule_swap(self, shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        ''' Performs a swap in workers for a shift, updates the workload of both workers in the process'''
        self.schedule_out(shift_id, Schedule)
        self.schedule_in(shift_id, employee_id, Schedule)

    """ MUTATE """

    def mutate(self, schedule: Schedule, T) -> list:
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # buds will be the mutated schedules
        buds = []
        old_cost = MalusCalc.get_total_cost(self.standard_cost, schedule)
        while len(buds) < 10:
            
            # copy the original schedule
            bud_schedule = Schedule(Workload(recursive_copy(schedule.Workload)), old_cost, recursive_copy(schedule))
            for i in range(schedule.MUTATIONS):
                buds = self.modification(buds, bud_schedule, old_cost, T)

        return buds
    
    def modification(self, buds, schedule, old_cost, T) -> Schedule:
        # find a modification            
        replace_shift_id = self.get_random_shift()
        current_employee_id = schedule[replace_shift_id]
        replace_employee_id = self.get_random_employee(replace_shift_id, current_employee_id, schedule)

        # check if new worker wants to work additional shift, if not, use mutate_max
        if schedule.Workload.check_capacity(replace_shift_id, replace_employee_id):

            if ShiftConstrains.passed_hard_constraints(replace_shift_id, replace_employee_id, schedule):
                self.schedule_swap(replace_shift_id, replace_employee_id, schedule)
                buds = self.accept_change(schedule, old_cost, buds, T)            
                
            return buds
        else: # if worker does not want an additional shift, have someone else work on of the worker's shift
            schedule = self.mutate_max_workload(replace_shift_id, replace_employee_id, schedule) 
            buds = self.accept_change(schedule, old_cost, buds, T)
            return buds
        
    def accept_change(self, bud_schedule: Schedule, old_cost: int, buds: list, T: float) -> list:
        ''' Method that evaluates if a mutated schedule will be accepted based on the new cost
            and a simulated annealing probability'''
        
        # store the costs in bud_schedule
        bud_schedule.cost = MalusCalc.get_total_cost(self.standard_cost, bud_schedule)
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
            print(get_shift(shift_id), get_employee(employee_id))
