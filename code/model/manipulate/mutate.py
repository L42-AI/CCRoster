import random
import math

from model.representation.behaviour_classes.shift_constraints import Shiftconstraints
from model.representation.behaviour_classes.malus_calc import MalusCalc
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.schedule import AbsSchedule, Plant
from model.manipulate.fill import Fill
from model.representation.behaviour_classes.shift_constraints import Shiftconstraints

from presentor.helpers import recursive_copy

""" MUTATE """
class Mutate(Fill):

    def __init__(self, employee_list, shift_list, standard_cost, shift_constraints):
        self.id_employee = {x.id:x for x in employee_list}
        self.id_shift = {x.id: x for x in shift_list}
        self.shift_list = shift_list
        self.standard_cost = standard_cost
        self.shift_constraints = shift_constraints

    def mutate(self, schedule: Plant, T: float) -> list[Plant]:
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # buds will be the mutated schedules
        buds = []
        old_cost = schedule.cost
        for i in range(100):
            if len(buds) > 9:
                continue
            
            # copy the original schedule
            bud_schedule = Plant(Workload(schedule.Workload.shift_list, schedule.Workload.employee_list, recursive_copy(schedule.Workload)), old_cost, recursive_copy(schedule))
            for _ in range(schedule.MUTATIONS):
                buds = self.modification(buds, bud_schedule, T)
        return buds

    def modification(self, buds: list[Plant], schedule: Plant, T: float) -> list[Plant]:
        # find a modification            
        replace_shift_id = self.get_random_shift(schedule.Workload.shift_list)
        current_employee_id = schedule[replace_shift_id]
        replace_employee_id = self.get_random_employee(replace_shift_id, current_employee_id)
        old_cost = schedule.cost

        # check if new worker wants to work additional shift, if not, use mutate_max
        if schedule.Workload.check_capacity(replace_shift_id, replace_employee_id):

            if self.shift_constraints.passed_hard_constraints(replace_shift_id, replace_employee_id, schedule):
                Fill.schedule_swap(replace_shift_id, replace_employee_id, schedule)
                buds = self.accept_change(schedule, old_cost, buds, T, shift_id=replace_shift_id, new_emp=replace_employee_id, old_emp=current_employee_id)            
                
            return buds
        else: # if worker does not want an additional shift, have someone else work on of the worker's shift
            schedule = self.mutate_max_workload(replace_shift_id, replace_employee_id, schedule) 
            buds = self.accept_change(schedule, old_cost, buds, T)
            ''' DOES THE ORIGINAL WORKER EVEN GET SCHEDULED IN THIS SCENARIO??'''
            return buds
    
    def accept_change(self, bud_schedule: Plant, old_cost: int, buds: list, T: float, shift_id: int=None, new_emp: int=None, old_emp: int=None) -> list:
        ''' Method that evaluates if a mutated schedule will be accepted based on the new cost
            and a simulated annealing probability'''
        if shift_id != None: # does not take into account 'free' hours
        #     # print(sum([self.id_shift[id_].duration for x in bud_schedule.Workload[new_emp] for id_ in bud_schedule.Workload[new_emp][x] if id_ != shift_id]), bud_schedule.Workload[new_emp][5])
        
            duration_old_emp, duration_new_emp = self._billable_hours(shift_id, old_emp, new_emp, bud_schedule)
            old_wage = self.id_employee[old_emp].wage
            new_wage = self.id_employee[new_emp].wage
            cost_old_emp = old_wage * duration_old_emp
            cost_new_emp = new_wage * duration_new_emp

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
    
    
    def mutate_max_workload(self, shift_to_replace_id: int, possible_employee_id: int, schedule: Plant) -> list[tuple[int, int]]:
        '''
        Method gets called when mutate wants to schedule a worker for a shift but the worker is already
        working his/hers max. This method will replace one of his/her shifts to check if that will be cheaper
        '''

        # get the shortest shift the busy person is working
        shifts_busy_person = [x for x in schedule if schedule[x] == possible_employee_id]
        if len(shifts_busy_person) == 0:
            return schedule
        shortest_shift_id = sorted(shifts_busy_person, key=lambda x: schedule.Workload.id_shift[x].duration)[0]

        # make sure we do not get stuck in recursive loop
        if shift_to_replace_id == shortest_shift_id:
            return schedule

        # pick new employee to work the shortest shift
        shortest_shift_employee_id = self.get_random_employee(shortest_shift_id, possible_employee_id)

        # check if worker that will take over the shift, still wants to work additional shift
        if schedule.Workload.check_capacity(shortest_shift_id, shortest_shift_employee_id):
            if self.shift_constraints.passed_hard_constraints(shortest_shift_id, shortest_shift_employee_id, schedule):

                self.schedule_swap(shortest_shift_id, shortest_shift_employee_id, schedule)

        # find replacement for the replacement worker
        else: 
            self.mutate_max_workload(shortest_shift_id, shortest_shift_employee_id, schedule)
        return schedule

    """ Helper methods """

    def _billable_hours(self, shift_id: int, old_emp: int, new_emp: int, bud_schedule: Plant):
            duration = self.id_shift[shift_id].duration
            duration_old_emp = max(0, duration - max(0, self.id_employee[old_emp].min_hours - sum([self.id_shift[id_].duration for x in bud_schedule.Workload[old_emp] for id_ in bud_schedule.Workload[old_emp][x]])))
            duration_new_emp = max(0, duration - max(0, self.id_employee[new_emp].min_hours - sum([self.id_shift[id_].duration for x in bud_schedule.Workload[new_emp] for id_ in bud_schedule.Workload[new_emp][x] if id_ != shift_id])))
            return duration_old_emp, duration_new_emp

    