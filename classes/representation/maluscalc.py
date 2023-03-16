from data.assign import employee_list
from data.queries import *

class MalusCalculator:
    def __init__(self, schedule, db, cursor) -> None:
        self.employee_dict = self.init_employee_dict(employee_list)
        self.schedule = schedule
        self.malus = 0
        self.db = db
        self.cursor = cursor
        self.get_wage_costs_per_week(self.schedule)

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
        wage_costs = self.get_wage_costs_per_week()

        print(f'Malus: {self.malus}')
        print(wage_costs)
        count = 0
        for key in wage_costs:
            if key.startswith('week'):
                count += 1
                print(f"Week {count} Costs: {wage_costs[key]['total']}")



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


    def get_wage_costs_per_week(self, schedule) -> dict:
        ''''
        JACOBS VERSION
        '''
        location = 1 # coffeecompany
        wage_employees = download_wages(self.db, self.cursor, location) # dictionary with id as key and wage as value
        wage_employees[0] = 100000
        wage_costs = {'schedule': 0.0}
        for shift in schedule:
            wage = wage_employees[shift[4]]
            if f'week {shift[0]}' not in wage_costs:
                wage_costs[f'week {shift[0]}'] = wage

            else:
                wage_costs[f'week {shift[0]}']+= wage
            wage_costs['schedule'] += wage
        print(wage_costs['schedule'])
        return wage_costs
        # '''
        # LUKAS VERSION
        # '''
        # wage_costs = {'schedule': 0.0}

        # for week_num, week in enumerate(self.schedule):

        #     if f'week {week_num}' not in wage_costs:
        #         wage_costs[f'week {week_num}'] = {}

        #     for day_num, day in enumerate(week):

        #         if 'total' not in wage_costs[f'week {week_num}']:
        #             wage_costs[f'week {week_num}']['total'] = 0.0

        #         if f'day {day_num}' not in wage_costs[f'week {week_num}']:
        #             wage_costs[f'week {week_num}'][f'day {day_num}'] = 0.0

        #         for shift_num, shift in enumerate(day):
        #             for employee_name in shift:

        #                 employee_obj = self.get_employee_object(employee_name)

        #                 wage_cost = employee_obj.get_wage() * DAILY_SHIFTS[f'shift {shift_num}']['duration']

        #                 wage_costs['schedule'] += wage_cost
        #                 wage_costs[f'week {week_num}'][f'day {day_num}'] += wage_cost
        #                 wage_costs[f'week {week_num}']['total'] += wage_cost

        # return wage_costs
