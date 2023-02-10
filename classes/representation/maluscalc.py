from data.assign import employee_list
from collections import Counter

class MalusCalculator:
    def __init__(self, schedule) -> None:
        self.employee_list = employee_list
        self.schedule = schedule
        self.malus = 0

    def calc_malus(self):
        self.weekly_max()

    def weekly_max(self):

        weekly_shift_dict = {}

        for week_num, week in enumerate(self.schedule):

            if week_num not in weekly_shift_dict:
                weekly_shift_dict[f'week {week_num}'] = {}

            for day in week:

                for shift in day:

                    for employee in shift:

                        if employee not in weekly_shift_dict[f'week {week_num}']:
                            weekly_shift_dict[f'week {week_num}'][employee] = 0
                        else:
                            weekly_shift_dict[f'week {week_num}'][employee] += 1

        print(weekly_shift_dict)

    def same_person(self, day):
        daily_workers = []
        for shift in day:
            for employee in shift:
                if employee in daily_workers:
                    self.malus += 1
                else:
                    daily_workers.append(employee)


