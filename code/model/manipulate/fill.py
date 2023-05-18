import random

from model.representation.behaviour_classes.shift_constraints import Shiftconstraints
from model.representation.data_classes.schedule import AbsSchedule, Schedule
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

""" Schedule manipulation """
class Fill:

    def __init__(self, shift_constraints: Shiftconstraints):
        self.shift_constraints = shift_constraints

    def schedule_in(shift_id: int, employee_id: int, Schedule: AbsSchedule) -> None:
        ''' Places a worker in a shift in the schedule, while also updating his workload '''
        Schedule[shift_id] = employee_id
        Schedule.Workload.update(shift_id, employee_id, add=True)

    def schedule_out(shift_id: int, Schedule: AbsSchedule) -> None:
        ''' Removes a worker from a shift and updates the workload so the worker has room to work another shift'''
        employee_id = Schedule[shift_id]
        Schedule[shift_id] = None
        Schedule.Workload.update(shift_id, employee_id, add=False)

    @staticmethod
    def schedule_swap(shift_id: int, employee_id: int, Schedule: AbsSchedule) -> None:
        ''' Performs a swap in workers for a shift, updates the workload of both workers in the process'''
        Fill.schedule_out(shift_id, Schedule)
        Fill.schedule_in(shift_id, employee_id, Schedule)

    def fill(self, Schedule: AbsSchedule):
        filled = 0

        while filled < len(Schedule):

            shift_id = self.get_random_shift(Schedule.Workload.shift_list)

            if Schedule[shift_id] is not None:
                continue

            employee_id = self.get_random_employee(shift_id)
            if Schedule.Workload.check_capacity(shift_id, employee_id):

                if self.shift_constraints.passed_hard_constraints(shift_id, employee_id, Schedule):
                    Fill.schedule_in(shift_id, employee_id, Schedule)
                    filled += 1
                    continue
                # else:
                #     Schedule = self.relieve_workload(shift_id, employee_id, Schedule)
                #     continue

        return Schedule
    
    def relieve_workload(self, shift_to_replace_id: int, possible_employee_id: int, schedule: AbsSchedule) -> list[tuple[int, int]]:
        '''
        Method gets called fill wants to assign an employee to a shift but he/she is already working his/hers max
        '''

        # get a shift from that person to free up
        shifts_busy_person = [x for x in schedule if schedule[x] == possible_employee_id]
        new_shift = random.choice(shifts_busy_person)

        # make sure we do not get stuck in recursive loop
        if shift_to_replace_id == new_shift:
            return schedule

        # pick new employee to work the shortest shift
        shortest_shift_employee_id = self.get_random_employee(new_shift, possible_employee_id)

        # check if worker that will take over the shift, still wants to work additional shift
        if schedule.Workload.check_capacity(new_shift, shortest_shift_employee_id):
            if self.shift_constraints.passed_hard_constraints(new_shift, shortest_shift_employee_id, schedule):

                Fill.schedule_swap(new_shift, shortest_shift_employee_id, schedule)
                
        # find replacement for the replacement worker
        else: 
            self.relieve_workload(new_shift, shortest_shift_employee_id, schedule)
        return schedule


    def get_random_shift(self, shift_list) -> int:
        """
        returns an int corresponding with a shift's id
        """

        shift_id = random.choice(shift_list).id
        return shift_id

    def get_random_employee(self, shift_id: int, existing_employee: int = None) -> int:
        """
        returns an employee id
        """

        if existing_employee != None:
            choices = self.shift_constraints.total_availabilities[shift_id] - {existing_employee}
        else:
            choices = self.shift_constraints.total_availabilities[shift_id]
        
        if not choices:
            raise ValueError("No available employees for shift")

        return random.choice(list(choices))


class Greedy(Fill):
    
    def __init__(self, shift_constraints):
        super().__init__(shift_constraints)

    def schedule_in(shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        Schedule[shift_id] = employee_id
        Schedule.Workload.update(shift_id, employee_id, add=True)

        week_num = Schedule.Workload.get_weeknumber(shift_id)
        employee_obj = Schedule.Workload.id_employee[employee_id]

        if len(Schedule.Workload[employee_id][week_num]) == employee_obj.get_week_max(week_num):
            Greedy.update_availabilty(Schedule, employee_id, shift_id, added=True, max_hit=True)
        else:
            Greedy.update_availabilty(Schedule, employee_id, shift_id, added=True, max_hit=False)

    def schedule_out(shift_id: int, Schedule: Schedule) -> None:
        employee_id = Schedule[shift_id]
        Schedule[shift_id] = None
        Schedule.Workload.update(shift_id, employee_id, add=False)

        Greedy.update_availabilty(Schedule, employee_id, shift_id, added=False)

    @staticmethod
    def schedule_swap(shift_id: int, employee_id: int, Schedule: Schedule) -> None:
        ''' Performs a swap in workers for a shift, updates the workload of both workers in the process'''
        Greedy.schedule_out(shift_id, Schedule)
        Greedy.schedule_in(shift_id, employee_id, Schedule)

    def update_availabilty(self, Schedule: Schedule, employee_id: int, shift_id: int, added: bool, max_hit: bool = False) -> None:

        Greedy.set_shift_occupation(Schedule, shift_id, added)
        coliding_shifts = self.shift_constraints.time_conflict_dict[shift_id]

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

    def set_shift_occupation(Schedule: Schedule, shift_id: int, occupied: bool) -> None:
        if occupied:
            Schedule.CurrentAvailabilities[shift_id][0] = 1
        else: 
            Schedule.CurrentAvailabilities[shift_id][0] = 0

    def fill(employee_list: list[Employee], shift_list: list[Shift], Schedule: Schedule) -> Schedule:

        filled = 0
        shift_id_list = [shift.id for shift in shift_list]
        while filled < len(Schedule):
            
            shift_id = sorted(shift_id_list, key=lambda x: len(Schedule.CurrentAvailabilities[x][1]) if Schedule.CurrentAvailabilities[x][0] == 0 else 999)[0]

            # Skip if shift scheduled
            if Schedule[shift_id] is not None:
                continue

            if len(Schedule.CurrentAvailabilities[shift_id][1]) < 1:
                raise LookupError('No availabilities for shift!')

            weeknum = Schedule.Workload.get_weeknumber(shift_id)

            Greedy.compute_priority(employee_list, Schedule, weeknum)
            Greedy.update_highest_priority_list(employee_list)

            possible_employee_ids = Schedule.CurrentAvailabilities[shift_id][1]
            selected_employee_id = random.choice(tuple(possible_employee_ids))
            
            for employee_id in possible_employee_ids:
                if Schedule.Workload.id_employee[employee_id].priority < Schedule.Workload.id_employee[selected_employee_id].priority:
                    selected_employee_id = employee_id
            
            Greedy.schedule_in(shift_id, selected_employee_id, Schedule)

            if not Shiftconstraints.passed_hard_constraints(shift_id, selected_employee_id, Schedule):
                Greedy.schedule_out(shift_id, Schedule)
            else:
                filled += 1

        return Schedule

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

    def update_highest_priority_list(employee_list: list[Employee]) -> None:
        return sorted(employee_list, key = lambda employee: employee.priority)
