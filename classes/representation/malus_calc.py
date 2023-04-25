from classes.representation.employee import Employee
from classes.representation.workload import Workload
from classes.representation.schedule import Schedule

from helpers import get_shift, get_employee, get_weeknumber, id_shift
from data.assign import employee_list


class MalusCalc:

    @staticmethod
    def compute_wage_cost(Schedule: Schedule) -> float:
        total_cost = 0
        for shift_id, employee_id in Schedule.items():
            total_cost += MalusCalc._compute_cost(Schedule.Workload, shift_id, employee_id)
        return round(total_cost, 2)
    
    @staticmethod
    def compute_replacement_factor(availabilities_dict: dict[int, set[int]]) -> float:

        max_len_shift = sorted(availabilities_dict, key = lambda shift_id: len(availabilities_dict[shift_id][1]), reverse=True)[0]
        min_len_shift = sorted(availabilities_dict, key = lambda shift_id: len(availabilities_dict[shift_id][1]))[0]

        max_len = len(availabilities_dict[max_len_shift][1])
        min_len = len(availabilities_dict[min_len_shift][1])
        
        return (max_len - min_len) / max (1, min_len)

    def compute_team_strength(self) -> float:
        ...

    @staticmethod
    def standard_cost(employee_list: list[Employee]):
        """
        calculates the total costs of a schedule
        """
        # calculate the starting costs
        total = sum([employee.get_minimal_hours() * employee.get_wage()  for employee in employee_list])

        return round(total, 2)
    
    @staticmethod
    def get_total_cost(standard_cost, Schedule: Schedule) -> float:
        wage_cost = MalusCalc.compute_wage_cost(Schedule)
        return round(wage_cost + standard_cost, 2)

    @staticmethod
    def _compute_cost(workload: Workload, shift_id: int, employee_id: int) -> float:
        """
        returns the total pay using the wage and shift in hours. Also takes into account that if an employee has a
        weekly min, the first shifts are 'free'
        """

        possible_employee_object = get_employee(employee_id)
        hours = get_shift(shift_id).duration
        weeknumber = get_weeknumber(shift_id)
        minimal_hours = possible_employee_object.get_minimal_hours()
        wage = possible_employee_object.get_wage()
        total_scheduled_duration = sum(get_shift(x).duration for x in workload[weeknumber])
        remaining_min_hours = minimal_hours - total_scheduled_duration if (minimal_hours - total_scheduled_duration) < 0 else 0


        return wage * (hours - remaining_min_hours) # Multiply duration with hourly wage to get total pay