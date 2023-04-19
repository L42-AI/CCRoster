

from data.assign import shift_list
from classes.representation.shift import Shift


class ShiftConstrains:
    def __init__(self) -> None:
        self.time_conflict_dict = self.init_coliding_dict(shift_list)

    def __getitem__(self, index: int) -> list[int]:
        if index not in self.time_conflict_dict:
            raise ValueError('Shift id not in conflicting shifts dict')
        return self.time_conflict_dict[index]


    """ INIT """

    @staticmethod
    def init_coliding_dict(shifts: list[Shift]) -> dict[int, list[int]]:

        time_conflict_dict = {shift.id: [] for shift in shifts}

        for i, shift_1 in enumerate(shifts):

            for shift_2 in shifts[i+1:]:
                if shift_1.end < shift_2.start:
                    continue
                if shift_1.start < shift_2.end:
                    time_conflict_dict[shift_1.id].append(shift_2.id)
                    time_conflict_dict[shift_2.id].append(shift_1.id)

        return time_conflict_dict

    """ GET """

    def get_colliding_shifts(self, shift_id: int) -> list[int]:
        return self.time_conflict_dict.get(shift_id)

    """ METHODS """

    def passed_hard_constraints(self, shift_id: int, employee_id: int, schedule: dict[int, int]) -> bool:
        if self._same_time(shift_id, employee_id, schedule):
            return False
        return True

    """ HELPER """

    def _same_time(self, shift_id: int, employee_id: int, schedule: dict[int, int]) -> bool:
        if employee_id is None:
            raise ValueError('No employee in the schedule')

        colliding_shifts = self.get_colliding_shifts(shift_id)
        for colliding_shift_id in colliding_shifts:
            if schedule[colliding_shift_id] == employee_id:
                return True

        return False