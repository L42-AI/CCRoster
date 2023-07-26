from datetime import datetime

from model.representation.data_classes.shift import Shift
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.schedule import Schedule

class ShiftConstraintsHelpers:
    @staticmethod
    def is_within_amount_of_days(dt1: datetime, dt2: datetime, k: int) -> bool:
        seconds = k * 86400
        return abs((dt1 - dt2).total_seconds()) <= seconds


class SoftShiftConstraints:
    """ Include all methods that deal with softcontraints """

    """ RECURRANCE """

    @staticmethod
    def passed_recurrance_check(existing_shift: Shift, new_shift: Shift, existing_employee_id: int, new_employee_id: int) -> bool:
        if ShiftConstraintsHelpers.is_within_amount_of_days(existing_shift.start, new_shift.start, 1):
            return False
        elif existing_shift.shift_type != new_shift.shift_type:
            return False
        elif existing_employee_id != new_employee_id:
            return False
        elif existing_shift.start.day == new_shift.start.day:
            return False
        return True
    
    @staticmethod
    def count_shift_recurrences(schedule: Schedule, id_shift: dict[int, Shift]) -> dict[int, dict[str, int]]:
        """
        Count the occurrences of type 1 and type 2 shifts for each employee in the schedule.
        """

        employee_recurrences = {}

        for shift_id in schedule:
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

            for shift_id in schedule:
                match_shift = id_shift[shift_id]

                if SoftShiftConstraints.passed_recurrance_check(shift, match_shift, employee_id, schedule.get(match_shift.id)):
                    employee_recurrences[employee_id][f"type_{dict_type}"] += 1

        return employee_recurrences

    @staticmethod
    def get_employee_recurrance_score(schedule: Schedule, id_shift: dict[int, Shift], employee_id: int) -> dict[str, int]:
        """
        Count the occurrences of type 1 and type 2 shifts for each employee in the schedule.
        """

        employee_recurrence = {"type_1": 0, "type_2": 0}

        all_shifts = list(schedule.keys())
        
        for shift_id in all_shifts:
            if schedule.get(shift_id) != employee_id:
                continue
            
            shift = id_shift[shift_id]

            if shift.shift_type == 0:
                continue
            elif shift.shift_type == 1:
                dict_type = 1
            elif shift.shift_type == 2:
                dict_type = 2

            for shift_id in all_shifts:
                match_shift = id_shift[shift_id]

                if SoftShiftConstraints.passed_recurrance_check(shift, match_shift, employee_id, employee_id):
                    employee_recurrence[f"type_{dict_type}"] += 1

        return employee_recurrence

    @staticmethod
    def creates_shift_reoccurance(new_shift_id: int, new_employee_id: int, schedule: Schedule, id_shift: dict[int, Shift]) -> bool:
        """
        Check if schedule change causes shift reoccurance
        """
        
        new_shift = id_shift[new_shift_id]

        # Skip regular shifts, reoccurance no problem
        if not new_shift.shift_type in [1, 2]:
            return False
    
        for shift_id, employee_id in schedule.items():
            scheduled_shift = id_shift[shift_id]

            if SoftShiftConstraints.passed_recurrance_check(scheduled_shift, new_shift, employee_id, new_employee_id):
                return False
            return True
        
    @staticmethod
    def warn_for_shift_recurrence() -> None:
        print('This change causes a shift reocurrance')

    @staticmethod
    def print_shift_recurrence_counts(schedule: Schedule, id_shift: dict[int, Shift], id_employee: dict[int, Employee]):
        """
        Print the shift recurrence counts for each employee in a human-readable format.
        """

        recurrence_counts = SoftShiftConstraints.count_shift_recurrences(schedule, id_shift)

        print("Shift Recurrence Counts:")
        for employee_id, counts in recurrence_counts.items():
            employee_name = id_employee.get(employee_id, "Unknown Employee")
            type_1_count = counts.get("type_1", 0)
            type_2_count = counts.get("type_2", 0)

            print(f"Employee ID: {employee_id}, Employee Name: {employee_name}")
            print(f"  Type 1 Shifts Recurrence Count: {type_1_count}")
            print(f"  Type 2 Shifts Recurrence Count: {type_2_count}")
            print("------------------------")

    """ FREE DAYS """

    @staticmethod
    def passed_free_days(schedule: Schedule, id_shift: dict[int, Shift], new_shift_id: int, new_employee_id: int, k: int):
        for scheduled_shift_id, scheduled_employee_id in schedule.items():
            if new_employee_id != scheduled_employee_id:
                continue
            if not ShiftConstraintsHelpers.is_within_amount_of_days(id_shift[scheduled_shift_id].start, id_shift[new_shift_id].start, k):
                continue
            return True
        return False
    
    @staticmethod
    def count_free_day_sequence_fail(schedule: Schedule, id_shift: dict[int, Shift], k: int):
        fail_counter = {}
        for first_shift_id, first_employee_id in schedule.items():
            for second_shift_id, second_employee_id in schedule.items():
                if second_employee_id != first_employee_id:
                    continue
                if ShiftConstraintsHelpers.is_within_amount_of_days(id_shift[first_shift_id].start, id_shift[second_shift_id].start, k):
                    if first_employee_id not in fail_counter:
                        fail_counter[first_employee_id] = 1
                    else:
                        fail_counter[first_employee_id] += 1 

                    


class HardShiftConstraints:
    
    @staticmethod
    def same_time(shift_id: int, employee_id: int, Schedule: Schedule, time_conflict_dict: dict[int, list[int]]) -> bool:
        if employee_id is None:
            raise ValueError('No employee in the schedule')

        colliding_shifts = time_conflict_dict[shift_id]
        for colliding_shift_id in colliding_shifts:
            if Schedule[colliding_shift_id] == employee_id:
                return True

        return False


class ShiftConstraints:

    @staticmethod
    def get_soft_constraints_score(schedule: Schedule, id_shift: dict[int, Shift], id_employee: dict[int, Employee]) -> float:
        score = {}
        
        for scheduled_shift_id, scheduled_employee_id in schedule.items():
            employee = id_employee[scheduled_employee_id]
            soft_constraints_profile = employee, NotImplemented

            match soft_constraints_profile:
                case 'All recurrance':
                    recurrance_score = SoftShiftConstraints.get_employee_recurrance_score(schedule, id_shift, scheduled_employee_id)
                    score[scheduled_employee_id] = sum(recurrance_score.values())
                case 'Opening Recurrance':
                    recurrance_score = SoftShiftConstraints.get_employee_recurrance_score(schedule, id_shift, scheduled_employee_id)
                    score[scheduled_employee_id] = recurrance_score.values()[0]
                case 'Closing Recurrance':
                    recurrance_score = SoftShiftConstraints.get_employee_recurrance_score(schedule, id_shift, scheduled_employee_id)
                    score[scheduled_employee_id] = recurrance_score.values()[1]
                case 'Free days':
                    free_day_dict = SoftShiftConstraints.count_free_day_sequence_fail(schedule, id_shift, 1) # Number gives the amount of free days in between shifts, should come from the db
                    score[scheduled_employee_id] = free_day_dict[scheduled_employee_id]




        recurrence_counts = SoftShiftConstraints.count_shift_recurrences(schedule, id_shift)
        for employee_id, recurrance_dict in recurrence_counts.items():
            employee = id_employee[employee_id]
            NotImplemented
    
    @staticmethod
    def passed_hard_constraints(shift_id: int, employee_id: int, schedule: Schedule, time_conflict_dict) -> bool:
        if HardShiftConstraints.same_time(shift_id, employee_id, schedule, time_conflict_dict):
            return False
        return True