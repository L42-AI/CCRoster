from datetime import datetime

from model.representation.data_classes.shift import Shift
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.schedule import Schedule

class ShiftConstrains:

    @staticmethod
    def soft_constraints_score() -> float:
        score = 1
        return score
    
    @staticmethod
    def print_shift_recurrence_counts(schedule: Schedule, id_shift: dict[int, Shift], id_employee: dict[int, Employee]):
        """
        Print the shift recurrence counts for each employee in a human-readable format.
        """

        recurrence_counts = ShiftConstrains.count_shift_recurrences(schedule, id_shift)

        print("Shift Recurrence Counts:")
        for employee_id, counts in recurrence_counts.items():
            employee_name = id_employee.get(employee_id, "Unknown Employee")
            type_1_count = counts.get("type_1", 0)
            type_2_count = counts.get("type_2", 0)

            print(f"Employee ID: {employee_id}, Employee Name: {employee_name}")
            print(f"  Type 1 Shifts Recurrence Count: {type_1_count}")
            print(f"  Type 2 Shifts Recurrence Count: {type_2_count}")
            print("------------------------")

    @staticmethod
    def warn_for_shift_recurrence() -> None:
        print('This change causes a shift reocurrance')

    @staticmethod
    def count_shift_recurrences(schedule: Schedule, id_shift: dict[int, Shift]) -> dict[int, dict[str, int]]:
        """
        Count the occurrences of type 1 and type 2 shifts for each employee in the schedule.
        """

        employee_recurrences = {}

        all_shifts = list(schedule.keys())
        
        for shift_id in all_shifts:
            shift = id_shift[shift_id]

            if shift.shift_type == 0:
                continue
            elif shift.shift_type == 1:
                dict_type = 1
            elif shift.shift_type == 2:
                dict_type = 2

            employee_id = schedule.get(shift_id)

            if employee_id not in employee_recurrences:
                employee_recurrences[employee_id] = {"type_1": 0, "type_2": 0}

            for shift_id in all_shifts:
                match_shift = id_shift[shift_id]

                if match_shift.shift_type != shift.shift_type:
                    continue

                if match_shift.start.day == shift.start.day:
                    continue

                if not ShiftConstrains.is_within_one_day(match_shift.start, shift.start):
                    continue

                if employee_id != schedule.get(match_shift.id):
                    continue

                employee_recurrences[employee_id][f"type_{dict_type}"] += 1

        return employee_recurrences

    @staticmethod
    def _creates_shift_reoccurance(new_shift_id: int, new_employee_id: int, schedule: Schedule, id_employee: dict[int, Employee], id_shift: dict[int, Shift]) -> bool:
        """
        Check if schedule change causes shift reoccurance
        """
        
        new_shift = id_shift[new_shift_id]

        # Skip regular shifts, reoccurance no problem
        if not new_shift.shift_type in [1, 2]:
            return False
    
        for shift_id, employee_id in schedule.items():
            scheduled_shift = id_shift[shift_id]

            if not ShiftConstrains.is_within_one_day(scheduled_shift.start, new_shift.start):
                continue
            
            if id_shift[shift_id].shift_type != new_shift.shift_type:
                continue

            if employee_id == new_employee_id and scheduled_shift.start.day != new_shift.start.day:
                return True
            

    @staticmethod
    def is_within_one_day(dt1: datetime, dt2: datetime) -> bool:
        # Check if the two datetimes are within one day of each other
        return abs((dt1 - dt2).total_seconds()) <= 86400  # 86400 seconds in a day


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

