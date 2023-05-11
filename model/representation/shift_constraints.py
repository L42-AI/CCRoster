from data.schedule_constants import time_conflict_dict
from model.representation.schedule import Schedule

from helpers import get_weeknumber, id_shift

class ShiftConstrains:

    @staticmethod
    def passed_hard_constraints(shift_id: int, employee_id: int, schedule: Schedule) -> bool:
        if ShiftConstrains.same_time(shift_id, employee_id, schedule, time_conflict_dict):
            return False
        return True

    @staticmethod
    def same_time(shift_id: int, employee_id: int, Schedule: Schedule, time_conflict_dict: dict[int, list[int]]) -> bool:
        if employee_id is None:
            raise ValueError('No employee in the schedule')

        colliding_shifts = time_conflict_dict[shift_id]
        for colliding_shift_id in colliding_shifts:
            if Schedule[colliding_shift_id] == employee_id:
                return True
            
        return False

    @staticmethod
    def is_shift_separated_by_one_day(shift_id: int, employee_id: int, Schedule: Schedule) -> bool:
        if employee_id is None:
            raise ValueError('No employee in the schedule')
        
        week_num = get_weeknumber(shift_id)
        shift_obj = id_shift[shift_id]
        working_shifts = Schedule.Workload[employee_id][week_num]

        for working_shift_id in working_shifts:
            working_shift_obj = id_shift[working_shift_id]
            if abs((working_shift_obj.end.date() - shift_obj.start.date()).days) >= 1:
                return True

        return False
