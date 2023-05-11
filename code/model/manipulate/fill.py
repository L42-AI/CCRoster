import random

from model.representation.behaviour_classes.shift_constraints import ShiftConstrains
from model.representation.data_classes.schedule import BaseSchedule
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

from model.representation.behaviour_classes.schedule_constants import time_conflict_dict

from helpers import get_weeknumber, id_employee

""" Schedule manipulation """

class Fill:

    @staticmethod
    def _schedule_in(shift_id: int, employee_id: int, Schedule: BaseSchedule) -> None:
        ''' Places a worker in a shift in the schedule, while also updating his workload '''
        Schedule[shift_id] = employee_id
        Schedule.Workload.update(shift_id, employee_id, add=True)

    @staticmethod
    def _schedule_out(shift_id: int, Schedule: BaseSchedule) -> None:
        ''' Removes a worker from a shift and updates the workload so the worker has room to work another shift'''
        employee_id = Schedule[shift_id]
        Schedule[shift_id] = None
        Schedule.Workload.update(shift_id, employee_id, add=False)

    @staticmethod
    def schedule_swap(shift_id: int, employee_id: int, Schedule: BaseSchedule) -> None:
        ''' Performs a swap in workers for a shift, updates the workload of both workers in the process'''
        Fill._schedule_out(shift_id, Schedule)
        Fill._schedule_in(shift_id, employee_id, Schedule)

class Greedy(Fill):

    @staticmethod
    def _schedule_in(shift_id: int, employee_id: int, Schedule: BaseSchedule) -> None:
        Schedule[shift_id] = employee_id
        Schedule.Workload.update(shift_id, employee_id, add=True)

        week_num = get_weeknumber(shift_id)
        employee_obj = id_employee[employee_id]

        if len(Schedule.Workload[employee_id][week_num]) == employee_obj.get_week_max(week_num):
            Greedy.update_availabilty(Schedule, employee_id, shift_id, added=True, max_hit=True)
        else:
            Greedy.update_availabilty(Schedule, employee_id, shift_id, added=True, max_hit=False)

    @staticmethod
    def _schedule_out(shift_id: int, Schedule: BaseSchedule) -> None:
        employee_id = Schedule[shift_id]
        Schedule[shift_id] = None
        Schedule.Workload.update(shift_id, employee_id, add=False)

        Greedy.update_availabilty(Schedule, employee_id, shift_id, added=False)

    @staticmethod
    def schedule_swap(shift_id: int, employee_id: int, Schedule: BaseSchedule) -> None:
        ''' Performs a swap in workers for a shift, updates the workload of both workers in the process'''
        Greedy._schedule_out(shift_id, Schedule)
        Greedy._schedule_in(shift_id, employee_id, Schedule)

    @staticmethod
    def update_availabilty(Schedule: BaseSchedule, employee_id: int, shift_id: int, added: bool, max_hit: bool = False) -> None:

        Greedy.set_shift_occupation(Schedule, shift_id, added)
        
        coliding_shifts = time_conflict_dict[shift_id]

        if added:
            for coliding_shift_id in coliding_shifts:
                if employee_id in Schedule.CurrentAvailabilities[coliding_shift_id][1]:
                    Schedule.CurrentAvailabilities[coliding_shift_id][1].remove(employee_id)
        
            if max_hit:
                for availability in Schedule.CurrentAvailabilities:
                    if employee_id in Schedule.CurrentAvailabilities[availability][1]:
                        Schedule.CurrentAvailabilities[availability][1].remove(employee_id)
        else:
            for availability in Schedule.CurrentAvailabilities:
                if employee_id in Schedule.CurrentAvailabilities[availability][1]:
                    Schedule.CurrentAvailabilities[availability][1].add(employee_id)

    @staticmethod
    def set_shift_occupation(Schedule: BaseSchedule, shift_id: int, occupied: bool) -> None:
        if occupied:
            Schedule.CurrentAvailabilities[shift_id][0] = 1
        else: 
            Schedule.CurrentAvailabilities[shift_id][0] = 0

    @staticmethod
    def greedy_fill(employee_list: list[Employee], shift_list: list[Shift], Schedule: BaseSchedule) -> BaseSchedule:

        filled = 0
        shift_id_list = [shift.id for shift in shift_list]
        while filled < len(Schedule):
            
            shift_id = sorted(shift_id_list, key=lambda x: len(Schedule.CurrentAvailabilities[x][1]) if Schedule.CurrentAvailabilities[x][0] == 0 else 999)[0]

            [print(Schedule.CurrentAvailabilities[shift_ID]) for shift_ID in Schedule.CurrentAvailabilities]
            print(shift_id)

            # Skip if shift scheduled
            if Schedule[shift_id] is not None:
                continue

            if len(Schedule.CurrentAvailabilities[shift_id][1]) < 1:
                raise LookupError('No availabilities for shift!')

            weeknum = get_weeknumber(shift_id)

            Greedy.compute_priority(employee_list, Schedule, weeknum)
            Greedy.update_highest_priority_list(employee_list)

            possible_employee_ids = Schedule.CurrentAvailabilities[shift_id][1]
            selected_employee_id = random.choice(tuple(possible_employee_ids))
            
            for employee_id in possible_employee_ids:
                if id_employee[employee_id].priority < id_employee[selected_employee_id].priority:
                    selected_employee_id = employee_id
            
            Greedy._schedule_in(shift_id, selected_employee_id, Schedule)

            if not ShiftConstrains.passed_hard_constraints(shift_id, selected_employee_id, Schedule):
                Greedy._schedule_out(shift_id, Schedule)
            else:
                filled += 1

        return Schedule

    @staticmethod
    def compute_priority(employee_list: list[Employee], Schedule: BaseSchedule, weeknum: int) -> None:
        for employee in employee_list:
            workload = Schedule.Workload[employee.id]
            week_max = employee.get_week_max(weeknum)
            week_min = employee.min_hours

            if weeknum in employee.availability:
                availability_priority = (len(employee.availability[weeknum]) - week_max)
                week_min_priority = (len(workload[weeknum]) - week_min)
                week_max_priority = (week_max - len(workload[weeknum]))
            
                if availability_priority < 1:
                    availability_priority = -99
                if week_min_priority < 0:
                    week_min_priority = -150
                if week_max_priority < 1:
                    week_max_priority = -99
                
                employee.priority = availability_priority + week_min_priority - week_max_priority
            else:
                employee.priority = 999

    @staticmethod
    def update_highest_priority_list(employee_list: list[Employee]) -> None:
        return sorted(employee_list, key = lambda employee: employee.priority)
