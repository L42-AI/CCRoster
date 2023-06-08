from model.representation.data_classes.availability import Availability
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

class ScheduleConstants:
    def get_standard_cost(employee_list: list[Employee]) -> float:
        """
        calculates the total costs of a schedule
        """
        # calculate the starting costs
        total = sum([employee.get_minimal_hours() * employee.get_wage()  for employee in employee_list])

        return round(total, 2)

    def get_coliding_dict(shifts_list: list[Shift]) -> dict[int, set[int]]:

        time_conflict_dict = {shift.id: set() for shift in shifts_list}

        for i, shift_1 in enumerate(shifts_list):

            for shift_2 in shifts_list[i+1:]:
                if shift_1.end < shift_2.start:
                    continue
                if shift_1.start < shift_2.end:
                    time_conflict_dict[shift_1.id].add(shift_2.id)
                    time_conflict_dict[shift_2.id].add(shift_1.id)

        return time_conflict_dict

    def get_total_availabilities(shift_list: list[Shift], employee_list: list[Employee]):
        return {shift.id: ScheduleConstants._get_employee_set(shift, employee_list) for shift in shift_list}

    def _possible_shift(workable_shift: Availability, employee: Employee, shift: Shift) -> bool:

        # Check time
        if workable_shift.start > shift.start or workable_shift.end < shift.end:
            return False

        # Check task
        tasks_list = employee.get_tasks()
        for task in tasks_list:
            if task == shift.task:
                return True
        return False

    def _get_employee_set(shift: Shift, employee_list: list[Employee]) -> set[int]:
        """
        this method is only used to develop the generator, later, the info will actually be downloaded
        for now it just returns a hardcoded list with availability
        """

        availabilities = set()
        for employee in employee_list:

            for weeknum in employee.availability_dict:
                for workable_shift in employee.availability_dict[weeknum]:

                    if ScheduleConstants._possible_shift(workable_shift, employee, shift):
                        availabilities.add(employee.id)

        return availabilities
    