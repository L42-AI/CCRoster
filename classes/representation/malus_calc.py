from classes.representation.employee import Employee
from classes.representation.workload import Workload
from classes.representation.schedule import Schedule

from helpers import get_shift, get_employee, get_weeknumber
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
        total = sum([sum(employee.weekly_min.values()) * employee.get_wage()  for employee in employee_list])

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
        weeknumber = get_weeknumber(shift_id)
        weekly_min = possible_employee_object.get_week_min(weeknumber)
        hours = get_shift(shift_id).duration
        wage = possible_employee_object.get_wage()

        # if week not in workload, number of shifts that week == 0
        if weeknumber not in workload[employee_id] and weekly_min > 0:

            # this shift the worker works for 'free'
            return 0

        # check if worker is under his/hers weely min
        elif len(workload[employee_id][weeknumber]) < weekly_min:
            return 0

        else:
            # if weekly_min is reached, calculate the wage it will cost normal way
            return wage * hours  # Multiply duration with hourly wage to get total pay