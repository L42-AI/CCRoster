from collections import defaultdict

from model.representation.data_objects import Employee
from representation.workload import Workload
from representation.schedule import Schedule

from helpers import get_weeknumber, id_shift, id_employee


class MalusCalc:

    # @staticmethod
    # def compute_wage_cost(Schedule: Schedule, skip_shift_id=None) -> float:
    #     total_cost = 0
    #     for shift_id, employee_id in Schedule.items():
    #         total_cost += MalusCalc._compute_cost(Schedule.Workload, shift_id, employee_id, skip_shift_id=skip_shift_id)
    #     return round(total_cost, 2)
    
    @staticmethod
    def compute_replacement_factor(availabilities_dict: dict[int, set[int]]) -> float:

        max_len_shift = sorted(availabilities_dict, key = lambda shift_id: len(availabilities_dict[shift_id][1]), reverse=True)[0]
        min_len_shift = sorted(availabilities_dict, key = lambda shift_id: len(availabilities_dict[shift_id][1]))[0]

        max_len = len(availabilities_dict[max_len_shift][1])
        min_len = len(availabilities_dict[min_len_shift][1])
        
        return (max_len - min_len) / max (1, min_len)

    def compute_team_strength(self) -> float:
        ...

    # @staticmethod
    # def get_total_cost(standard_cost: int, Schedule: Schedule, skip_shift_id=None) -> float:
    #     wage_cost = MalusCalc.compute_wage_cost(Schedule, skip_shift_id=skip_shift_id)
        
    #     return round(wage_cost + standard_cost, 2)

    @staticmethod
    def _compute_cost(workload: Workload, shift_id: int, employee_id: int, skip_shift_id=None) -> float:
        """
        returns the total pay using the wage and shift in hours. Also takes into account that if an employee has a
        a guaranteed working hours, those hours are 'free'
        """

        employee_obj = id_employee[employee_id]
        weeknumber = get_weeknumber(shift_id)
        minimal_hours = employee_obj.get_minimal_hours()
        hours = id_shift[shift_id].duration
        wage = employee_obj.get_wage()

        # check if employee has obligated contract hours left
        total_scheduled_duration = sum(id_shift[x].duration for x in workload[weeknumber] if x != skip_shift_id)
        remaining_min_hours = minimal_hours - total_scheduled_duration if (minimal_hours - total_scheduled_duration) > 0 else 0

        # subtract those hours, which are part of generator.standard_cost, from working hours to avoid double counting
        billable_hours = hours - remaining_min_hours if hours - remaining_min_hours > 0 else 0

        return wage * billable_hours # Multiply duration with hourly wage to get total pay
    
    def compute_cost(standard_cost: int, schedule: Schedule) -> float:
        wage_costs = 0

        employee_duration = defaultdict(float)
        for shift_id in schedule:
            employee_duration[schedule[shift_id]] += id_shift[shift_id].duration

        for employee, duration in employee_duration.items():
            employee_obj = id_employee[employee]
            wage_costs += max(duration - employee_obj.min_hours, 0) * employee_obj.get_wage()

        return round(wage_costs + standard_cost, 2)


        