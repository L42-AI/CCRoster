import random

from model.representation.behaviour_classes.shift_constraints import ShiftConstrains
from model.representation.data_classes.current_availabilities import CurrentAvailabilities
from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

from helpers import get_random_shift

""" Schedule manipulation """

class Fill:

    def __init__(self, total_availabilities: dict, time_conflict_dict: dict, id_employee, id_shift) -> None:
        self.total_availabilities = total_availabilities
        self.time_conflict_dict = time_conflict_dict
        self.id_employee_dict = id_employee
        self.id_shift_dict = id_shift

    """ Main """

    def generate(self, employee_list: list[Employee], shift_list: list[Shift]):
        schedule = Schedule(Workload(employee_list, shift_list), CurrentAvailabilities(self.total_availabilities))
        filled = 0
        while filled < len(schedule):
            shift_id = get_random_shift(schedule.Workload.shift_list)

            if schedule[shift_id] is not None:
                continue

            employee_id = self.get_random_employee(shift_id)
            # check if new worker wants to work additional shift, if not, use mutate_max
            if schedule.Workload.check_capacity(shift_id, employee_id):

                if ShiftConstrains.passed_hard_constraints(shift_id, employee_id, schedule, self.time_conflict_dict):
                    Fill.schedule_in(shift_id, employee_id, schedule)
                    filled += 1
                    continue

        return schedule

    """ Helpers """

    def schedule_in(shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        ''' Places a worker in a shift in the schedule, while also updating his workload '''
        Schedule[shift_id] = employee_id
        Schedule.Workload.update(shift_id, employee_id, add=True)

    def schedule_out(shift_id: int, Schedule: Schedule) -> None:
        ''' Removes a worker from a shift and updates the workload so the worker has room to work another shift'''
        employee_id = Schedule[shift_id]
        Schedule[shift_id] = None
        Schedule.Workload.update(shift_id, employee_id, add=False)

    def schedule_swap(shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        ''' Performs a swap in workers for a shift, updates the workload of both workers in the process'''
        Fill.schedule_out(shift_id, Schedule)
        Fill.schedule_in(shift_id, employee_id, Schedule)

    def get_random_employee(self, shift_id: int, existing_employee: int = None) -> int:
        """
        returns an employee id
        """

        if existing_employee != None:
            choices = self.total_availabilities[shift_id] - {existing_employee}
        else:
            choices = self.total_availabilities[shift_id]
        
        if not choices:
            raise ValueError("No available employees for shift")

        return random.choice(list(choices))

    def get_weeknumber(self, shift_id: int) -> int:
        shift_obj = self.id_shift_dict[shift_id]
        return shift_obj.start.isocalendar()[1]

class Greedy(Fill):

    def __init__(self, total_availabilities: dict, time_conflict_dict: dict, id_employee: dict[int, Employee], id_shift: dict[int, Shift]) -> None:
        super().__init__(total_availabilities, time_conflict_dict, id_employee, id_shift)

    """ Main """

    def generate(self, employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:

        schedule = Schedule(Workload(employee_list, shift_list), CurrentAvailabilities(self.total_availabilities))

        filled = 0
        shift_id_list = [shift.id for shift in shift_list]
        while filled < len(schedule):
            
            # print(schedule.CurrentAvailabilities[8])
            
            shift_id = sorted(shift_id_list, key=lambda x: len(schedule.CurrentAvailabilities[x][1]) if schedule.CurrentAvailabilities[x][0] == 0 else 999)[0]

            # Skip if shift scheduled
            if schedule[shift_id] is not None:
                continue

            if len(schedule.CurrentAvailabilities[shift_id][1]) < 1:
                raise LookupError('No availabilities for shift!')

            weeknum = self.get_weeknumber(shift_id)

            Greedy.compute_priority(employee_list, schedule, weeknum)
            Greedy.update_highest_priority_list(employee_list)

            possible_employee_ids = schedule.CurrentAvailabilities[shift_id][1]
            selected_employee_id = random.choice(tuple(possible_employee_ids))
            
            for employee_id in possible_employee_ids:
                if self.id_employee_dict[employee_id].priority < self.id_employee_dict[selected_employee_id].priority:
                    selected_employee_id = employee_id
            
            self.schedule_in(shift_id, selected_employee_id, schedule)

            if not ShiftConstrains.passed_hard_constraints(shift_id, selected_employee_id, schedule, self.time_conflict_dict):
                self.schedule_out(shift_id, schedule)
            else:
                filled += 1

        return schedule

    """ Helpers """

    def schedule_in(self, shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        Schedule[shift_id] = employee_id
        Schedule.Workload.update(shift_id, employee_id, add=True)

        week_num = self.get_weeknumber(shift_id)
        employee_obj = self.id_employee_dict[employee_id]

        if len(Schedule.Workload[employee_id][week_num]) == employee_obj.get_week_max(week_num):
            self.update_availabilty(Schedule, employee_id, shift_id, added=True, max_hit=True)
        else:
            self.update_availabilty(Schedule, employee_id, shift_id, added=True, max_hit=False)

    def schedule_out(self, shift_id: int, Schedule: Schedule) -> None:
        employee_id = Schedule[shift_id]
        Schedule[shift_id] = None
        Schedule.Workload.update(shift_id, employee_id, add=False)

        self.update_availabilty(Schedule, employee_id, shift_id, added=False)

    def update_availabilty(self, Schedule: Schedule, employee_id: int, shift_id: int, added: bool, max_hit: bool = False) -> None:

        Greedy.set_shift_occupation(Schedule, shift_id, added)
        
        coliding_shifts = self.time_conflict_dict[shift_id]

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
    def set_shift_occupation(Schedule: Schedule, shift_id: int, occupied: bool) -> None:
        if occupied:
            Schedule.CurrentAvailabilities[shift_id][0] = 1
        else: 
            Schedule.CurrentAvailabilities[shift_id][0] = 0

    @staticmethod
    def compute_priority(employee_list: list[Employee], Schedule: Schedule, weeknum: int) -> None:
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
