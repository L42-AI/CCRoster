import random
import math

from model.representation.behaviour_classes import ShiftConstrains, MalusCalc
from model.representation.data_classes import CurrentAvailabilities, Workload, Plant
from model.manipulate import Fill

from helpers import recursive_copy, get_random_employee_id, get_random_shift_id, gen_total_availabilities, gen_time_conflict_dict

""" MUTATE """

def mutate(schedule: Plant, T: float) -> list[Plant]:
    '''
    makes mutations to the schedule but remembers original state and returns to it if
    change is not better. So no deepcopies needed :0
    '''

    # buds will be the mutated schedules
    buds = []
    old_cost = MalusCalc.compute_cost(schedule)

    employee_list = schedule.Workload.employee_list
    shift_list = schedule.Workload.shift_list

    while len(buds) < 10:
        
        # copy the original schedule
        bud_schedule = Plant(
            Workload(employee_list, shift_list, recursive_copy(schedule.Workload)),
            CurrentAvailabilities(gen_total_availabilities(employee_list, shift_list)),
            old_cost,
            recursive_copy(schedule))
        for _ in range(schedule.MUTATIONS):
            buds = modification(buds, bud_schedule, T)
    return buds

def modification(buds: list[Plant], schedule: Plant, T: float) -> list[Plant]:
    # find a modification            
    replace_shift_id = get_random_shift_id(schedule.Workload.shift_list)
    current_employee_id = schedule[replace_shift_id]
    replace_employee_id = get_random_employee_id(schedule.CurrentAvailabilities.total_availabilities, replace_shift_id, current_employee_id)
    old_cost = schedule.cost

    # check if new worker wants to work additional shift, if not, use mutate_max
    if schedule.Workload.check_capacity(replace_shift_id, replace_employee_id):

        if ShiftConstrains.passed_hard_constraints(replace_shift_id, replace_employee_id, schedule, gen_time_conflict_dict(schedule.Workload.shift_list)):
            Fill.schedule_swap(replace_shift_id, replace_employee_id, schedule)
            buds = accept_change(schedule, old_cost, buds, T, shift_id=replace_shift_id, new_emp=replace_employee_id, old_emp=current_employee_id)            
            
        return buds
    else: # if worker does not want an additional shift, have someone else work on of the worker's shift
        schedule = mutate_max_workload(replace_shift_id, replace_employee_id, schedule) 
        buds = accept_change(schedule, old_cost, buds, T)
        return buds
    
def accept_change(bud_schedule: Plant, old_cost: int, buds: list, T: float, shift_id: int=None, new_emp: int=None, old_emp: int=None) -> list:
    ''' Method that evaluates if a mutated schedule will be accepted based on the new cost
        and a simulated annealing probability'''
    
    if shift_id != None: # does not take into account 'free' hours
    #     # print(sum([self.id_shift[id_].duration for x in bud_schedule.Workload[new_emp] for id_ in bud_schedule.Workload[new_emp][x] if id_ != shift_id]), bud_schedule.Workload[new_emp][5])
    
        duration_old_emp, duration_new_emp = _billable_hours(shift_id, old_emp, new_emp, bud_schedule)
        old_wage = bud_schedule.Workload.id_employee[old_emp].wage
        new_wage = bud_schedule.Workload.id_employee[new_emp].wage
        cost_old_emp = old_wage * duration_old_emp
        cost_new_emp = new_wage * duration_new_emp

        # print(old_cost - MalusCalc.compute_final_costs(self.standard_cost, bud_schedule), cost_old_emp - cost_new_emp)
        bud_schedule.cost = old_cost - cost_old_emp + cost_new_emp

    else:
        bud_schedule.cost = MalusCalc.compute_cost(bud_schedule)
    
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

def mutate_max_workload(shift_to_replace_id: int, possible_employee_id: int, schedule: Plant) -> list[tuple[int, int]]:
    '''
    Method gets called when mutate wants to schedule a worker for a shift but the worker is already
    working his/hers max. This method will replace one of his/her shifts to check if that will be cheaper
    '''

    # get the shortest shift the busy person is working
    shortest_shift_id = sorted(schedule.Workload.shift_list, key=lambda x: x.duration)[0].id

    # make sure we do not get stuck in recursive loop
    if shift_to_replace_id == shortest_shift_id:
        return schedule

    # pick new employee to work the shortest shift
    shortest_shift_employee_id = get_random_employee_id(schedule.CurrentAvailabilities.total_availabilities, shortest_shift_id, possible_employee_id)

    # check if worker that will take over the shift, still wants to work additional shift
    if schedule.Workload.check_capacity(shortest_shift_id, shortest_shift_employee_id):
        if ShiftConstrains.passed_hard_constraints(shortest_shift_id, shortest_shift_employee_id, schedule, gen_time_conflict_dict(schedule.Workload.shift_list)):

            Fill.schedule_swap(shortest_shift_id, shortest_shift_employee_id, schedule)

    # find replacement for the replacement worker
    else: 
        mutate_max_workload(shortest_shift_id, shortest_shift_employee_id, schedule)
    return schedule

""" Helper methods """

def _billable_hours(shift_id: int, old_emp: int, new_emp: int, bud_schedule: Plant):
        
        id_shift_dict = bud_schedule.Workload.id_shift
        id_employee_dict = bud_schedule.Workload.id_employee

        duration = id_shift_dict[shift_id].duration
        duration_old_emp = max(0, duration - max(0, id_employee_dict[old_emp].min_hours - sum([id_shift_dict[id_].duration for x in bud_schedule.Workload[old_emp] for id_ in bud_schedule.Workload[old_emp][x]])))
        duration_new_emp = max(0, duration - max(0, id_employee_dict[new_emp].min_hours - sum([id_shift_dict[id_].duration for x in bud_schedule.Workload[new_emp] for id_ in bud_schedule.Workload[new_emp][x] if id_ != shift_id])))
        return duration_old_emp, duration_new_emp