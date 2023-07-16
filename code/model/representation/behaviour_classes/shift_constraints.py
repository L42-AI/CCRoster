from model.representation.data_classes.schedule import Schedule

class ShiftConstrains:

    @staticmethod
    def passed_hard_constraints(shift_id: int, employee_id: int, schedule: Schedule, time_conflict_dict) -> bool:
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

