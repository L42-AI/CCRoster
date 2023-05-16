from collections import defaultdict

from model.representation.data_classes.employee import Employee
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.schedule import AbsSchedule

class MalusCalc:
    
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

      
    def compute_cost(standard_cost: int, schedule: AbsSchedule, plants) -> float:
        wage_costs = 0

        employee_duration = defaultdict(float)
        try:
            for shift_id in schedule:
                employee_duration[schedule[shift_id]] += schedule.Workload.id_shift[shift_id].duration
        except:
            print(schedule)
            print(plants)
            quit()
        for employee, duration in employee_duration.items():
            employee_obj = schedule.Workload.id_employee[employee]
            wage_costs += max(duration - employee_obj.min_hours, 0) * employee_obj.get_wage()

        return round(wage_costs + standard_cost, 2)

    def get_standard_cost(employee_list: list[Employee]) -> float:
        """
        calculates the standard costs of a schedule
        """
        # calculate the starting costs
        total = sum([employee.get_minimal_hours() * employee.get_wage()  for employee in employee_list])

        return round(total, 2)

        