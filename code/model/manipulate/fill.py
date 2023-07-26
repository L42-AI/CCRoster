import random
from pprint import pprint


from model.representation.behaviour_classes import ShiftConstraints

from model.representation.data_classes.current_availabilities import CurrentAvailabilities
from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.shift import Shift
from model.representation.data_classes.employee import Employee

from helpers import get_random_shift_id, compute_prob, softmax_function

""" Schedule manipulation """

class Fill:

    def __init__(self, total_availabilities: dict[int, dict[int, int]], time_conflict_dict: dict[int, set[int]], id_employee: dict[int, Employee], id_shift: dict[int, Shift]) -> None:
        self.total_availabilities = total_availabilities
        self.time_conflict_dict = time_conflict_dict
        self.id_employee_dict = id_employee
        self.id_shift_dict = id_shift

    """ Main """

    def generate(self, employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:
        schedule = Schedule(Workload(employee_list, shift_list), CurrentAvailabilities(self.total_availabilities))
        filled = 0
        while filled < len(schedule):
            shift_id = get_random_shift_id(shift_list)

            if schedule[shift_id] is not None:
                continue

            employee_id = self.get_random_employee(shift_id)
            # check if new worker wants to work additional shift, if not, use mutate_max
            if schedule.Workload.check_capacity(shift_id, employee_id):

                if ShiftConstraints.passed_hard_constraints(shift_id, employee_id, schedule, self.time_conflict_dict):
                    Fill.schedule_in(shift_id, employee_id, schedule)
                    filled += 1
                    continue

        return schedule

    """ Helpers """
    @staticmethod
    def schedule_in(shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        ''' Places a worker in a shift in the schedule, while also updating his workload '''
        Schedule[shift_id] = employee_id
        Schedule.Workload.update(shift_id, employee_id, add=True)

    @staticmethod
    def schedule_out(shift_id: int, Schedule: Schedule) -> None:
        ''' Removes a worker from a shift and updates the workload so the worker has room to work another shift'''
        employee_id = Schedule[shift_id]
        Schedule[shift_id] = None
        Schedule.Workload.update(shift_id, employee_id, add=False)

    @staticmethod
    def schedule_swap(shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        ''' Performs a swap in workers for a shift, updates the workload of both workers in the process'''
        Fill.schedule_out(shift_id, Schedule)
        Fill.schedule_in(shift_id, employee_id, Schedule)

    def get_random_employee(self, shift_id: int, existing_employee: int | None = None) -> int:
        """
        returns an employee id
        """

        choices = [emp for emp in self.total_availabilities[shift_id].keys() if emp != existing_employee]

        if len(choices) == 0:
            raise ValueError("No available employees for shift")

        return random.choice(choices)

    def get_weeknumber(self, shift_id: int) -> int:
        shift_obj = self.id_shift_dict[shift_id]
        return shift_obj.start.isocalendar()[1]

class Greedy(Fill):

    """ Main """

    def generate(self, employee_list: list[Employee], shift_list: list[Shift], weights: dict[int, dict[int, int]] | None = None) -> Schedule:

        schedule = Schedule(Workload(employee_list, shift_list), CurrentAvailabilities(self.total_availabilities))

        filled = 0
        shift_id_list = [shift.id for shift in shift_list]
        while filled < len(schedule):
            # print(schedule.CurrentAvailabilities[8])
            
            shift_id = sorted(shift_id_list, key=lambda x: len(schedule.CurrentAvailabilities[x][1]) if schedule.CurrentAvailabilities[x][0] == 0 else 999)[0]

            # Skip if shift scheduled
            if schedule[shift_id] is not None:
                continue

            if len(schedule.CurrentAvailabilities[shift_id][1].keys()) < 1:
                # print(f'No availabilities for shift id: {shift_id}!')
                return schedule

            if weights is not None:
                # Greedy.reset_weights(schedule, shift_id)
                Greedy.apply_weights(schedule, weights)

            possible_employee_ids = list(schedule.CurrentAvailabilities[shift_id][1].keys())
            possible_employee_weights = list(schedule.CurrentAvailabilities[shift_id][1].values())
            selected_employee_id = random.choices(possible_employee_ids, possible_employee_weights)[0]
            
            self.schedule_in(shift_id, selected_employee_id, schedule)

            if not ShiftConstraints.passed_hard_constraints(shift_id, selected_employee_id, schedule, self.time_conflict_dict):
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
                    Schedule.CurrentAvailabilities[coliding_shift_id][1].pop(employee_id)
        
            if max_hit:
                for availability in Schedule.CurrentAvailabilities:
                    if employee_id in Schedule.CurrentAvailabilities[availability][1]:
                        Schedule.CurrentAvailabilities[availability][1].pop(employee_id)
        else:
            # NEEDS TO BE DEPENDENT OF TOTAL AVAILABILITIES
            for availability in Schedule.CurrentAvailabilities:
                if employee_id in Schedule.CurrentAvailabilities[availability][1]:
                    print('readded')
                    Schedule.CurrentAvailabilities[availability][1][employee_id] = 0

    @staticmethod
    def set_shift_occupation(Schedule: Schedule, shift_id: int, occupied: bool) -> None:
        if occupied:
            Schedule.CurrentAvailabilities[shift_id][0] = 1
        else: 
            Schedule.CurrentAvailabilities[shift_id][0] = 0

    @staticmethod
    def reset_weights(Schedule: Schedule, shift_id: int):
        new_weight = 1 / len(Schedule.CurrentAvailabilities[shift_id][1].keys())
        for employee_id in Schedule.CurrentAvailabilities[shift_id][1]:
            Schedule.CurrentAvailabilities[shift_id][1][employee_id] = new_weight

    @staticmethod
    def apply_weights(Schedule: Schedule, weights: dict[int, dict[int, int]]):
        for shift_id in Schedule.CurrentAvailabilities:
            for employee_id in Schedule.CurrentAvailabilities[shift_id][1]:
                Schedule.CurrentAvailabilities[shift_id][1][employee_id] = weights[shift_id][employee_id]
