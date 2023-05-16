from model.representation.data_classes.schedule import AbsSchedule
from model.representation.data_classes.shift import Shift
from model.representation.data_classes.employee import Employee, Availability

class Shiftconstraints:
    def __init__(self, shift_list, employee_list):
    
        self.time_conflict_dict = Shiftconstraints.init_coliding_dict(shift_list)
        self.total_availabilities = {shift.id: Shiftconstraints.get_employee_set(shift, employee_list) for shift in shift_list}


    @staticmethod
    def get_employee_set(shift: Shift, employee_list: list[Employee]) -> set[int]:
        """
        this method is only used to develop the generator, later, the info will actually be downloaded
        for now it just returns a hardcoded list with availability
        """
        availabilities = set()
        for employee in employee_list:
            
            
            for weeknum in employee.availability_dict:
                for workable_shift in employee.availability_dict[weeknum]:
                    if Shiftconstraints._possible_shift(workable_shift, employee, shift):

                        availabilities.add(employee.id)
        return availabilities

    @staticmethod
    def init_coliding_dict(shifts) -> dict[int, set[int]]:

        time_conflict_dict = {shift.id: set() for shift in shifts}

        for i, shift_1 in enumerate(shifts):

            for shift_2 in shifts[i+1:]:
                if shift_1.end < shift_2.start:
                    continue
                if shift_1.start < shift_2.end:
                    time_conflict_dict[shift_1.id].add(shift_2.id)
                    time_conflict_dict[shift_2.id].add(shift_1.id)

        return time_conflict_dict

    def passed_hard_constraints(self, shift_id: int, employee_id: int, schedule: dict[int, int]) -> bool:
        if Shiftconstraints.same_time(shift_id, employee_id, schedule, self.time_conflict_dict):
            return False
        return True

    @staticmethod
    def same_time(shift_id: int, employee_id: int, Schedule: AbsSchedule, time_conflict_dict: dict[int, list[int]]) -> bool:
        if employee_id is None:
            raise ValueError('No employee in the schedule')

        colliding_shifts = time_conflict_dict[shift_id]
        for colliding_shift_id in colliding_shifts:
            if Schedule[colliding_shift_id] == employee_id:
                return True

        return False

    @staticmethod
    def _possible_shift(workable_shift: Availability, employee: Employee, shift: Shift) -> bool:

        # Check time
        if workable_shift.start > shift.start or workable_shift.end < shift.end:
            return False
        # Check task
        tasks_list = employee.get_tasks()

        for task in tasks_list:
            if task.task == shift.task:
                return True
        return False