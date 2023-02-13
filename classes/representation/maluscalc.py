from data.assign import employee_list
from classes.representation.GUI_output import DAILY_SHIFTS_TIME

class MalusCalculator:
    def __init__(self, schedule) -> None:
        self.employee_list = employee_list
        self.employee_dict = self.init_employee_dict(employee_list)
        self.schedule = schedule
        self.malus = 0
        self.costs = 0

    """ Init """

    def init_employee_dict(self, employee_list):
        dictionary = {}
        for employee in employee_list:
            dictionary[employee.get_name()] = employee
        return dictionary

    """ Get """

    def get_employee_object(self, name) -> object:
        return self.employee_dict.get(name)

    """ Methods """

    def calc_malus(self):
        weekly_shift_dict = self.weekly_max()
        self.compute_weekly_malus(weekly_shift_dict)
        print(self.malus)


    def weekly_max(self) -> dict:

        weekly_shift_dict = {}

        for week_num, week in enumerate(self.schedule):

            if week_num not in weekly_shift_dict:
                weekly_shift_dict[f'week {week_num}'] = {}

            for day in week:

                daily_workers = []

                for shift in day:

                    for employee in shift:

                        if employee in daily_workers:
                            self.malus += 1
                        else:
                            daily_workers.append(employee)

                        if employee not in weekly_shift_dict[f'week {week_num}']:
                            weekly_shift_dict[f'week {week_num}'][employee] = 0
                        else:
                            weekly_shift_dict[f'week {week_num}'][employee] += 1
        return weekly_shift_dict

    def compute_weekly_malus(self, weekly_shift_dict: dict):
        for week in weekly_shift_dict:
            for employee_name in weekly_shift_dict[week]:
                employee_object = self.get_employee_object(employee_name)

                week_max = employee_object.get_week_max(int(week[-1]))

                week_max_difference = weekly_shift_dict[week][employee_name] - week_max

                self.malus += week_max_difference if week_max_difference > 0 else 0


    """ Not working """
    def get_wage_costs_per_week(self) -> float:
        wage_costs = 0.0
        for week_num, week in enumerate(self.schedule):
            for day_num, day in enumerate(week):
                for shift_num, shift in enumerate(day):
                    for employee in shift:
                        wage_costs += employee.get_wage() * DAILY_SHIFTS_TIME[shift_num]
        return wage_costs
