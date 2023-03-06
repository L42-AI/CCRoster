from datetime import date, timedelta
import numpy as np
import random
import mysql.connector

from classes.representation.maluscalc import MalusCalculator
from classes.algorithms.switch import Switch
from classes.representation.GUI_output import SCHEDULE_DAYS, DAILY_SHIFTS, EMPLOYEE_PER_SHIFT
from data.queries import *

class Generator:
    def __init__(self) -> None:
        self.db, self.cursor = db_cursor()
        self.available_employees = [] # list with all employees that can work the shift with the same index in schedule
        self.schedule = self.init_schedule() # array with shifts that need to be filled

        self.availability =  0
        self.availability = self.init_availability() # array with all shifts that each employee can fill
        print('init!')
        # print(self.available_employees)
        # self.improve()
    """ INIT """

    def init_schedule(self) -> object:
        """
        Initiate the schedule
        """

        # get list of tuples of shifts needed
        shifts_needed = downloading_shifts(self.db, self.cursor)
        columns = len(shifts_needed[1]) + 1 # from shifts needed we do not need start and end but we add 3 new
        schedule = np.zeros((len(shifts_needed), columns))

        # transfer to np.array
        days = set()
        shift = 0
        for _, row in enumerate(shifts_needed):
            # set the day
            week = row[0]
            day = row[1]

            # count what shift it is
            if (week, day) not in days:
                shift = 0
                days.add((week, day))
            else:
                shift += 1
            task = row[4]

            # add info to schedule
            ## week, day, shift, task, employee_id, index
            schedule[_] = (week, day, shift, task, 0, int(_))

            # collect all employees that can work this shift
            self.available_employees.append(employee_per_shift(self.db, self.cursor, schedule[_]))

        return schedule

    def init_availability(self): # not being used right now!!!
        '''
        returns a list of availability per employee
        '''
        availability_data = downloading_availability(self.db, self.cursor)
        availability = np.zeros((len(availability_data), 5))
        for _, entry in enumerate(availability_data):
            id = entry[0]
            week = (entry[1] + 1)
            day = (entry[2] + 1)
            shift = entry[3]
            task = get_task(self.db, self.cursor, id)
            availability[_] = (week, day, shift, task, id)

        return availability
    """ GET """

    def get_date(self) -> object:
        """
        Find the current date
        """
        return date.today()

    def get_day(self, date) -> str:
        """
        Find the day of a certain date
        """
        return date.strftime("%A")

    def get_start_day(self) -> object:
        """
        Find date of start of schedule as the first Monday of the current month
        """
        return self.get_schedule_boundary(start=True)

    def get_end_day(self) -> object:
        """
        Find date of end of schedule as the first Monday of the next month
        """
        return self.get_schedule_boundary(start=False)

    def get_schedule_boundary(self, start):
        """
        Find date of start or end of schedule
        """

        # Set todays date
        today = date.today()

        if start:
            # Set date of the first day of the month
            interest_date = date(today.year, today.month, 1)
        else:
            # Set date of the first day of the next month
            next_month_date = today.replace(day=28) + timedelta(days=4)
            interest_date = date(next_month_date.year, next_month_date.month, 1)

        # Find closest Monday and set output date
        days_to_monday = (7 - interest_date.weekday()) % 7
        interest_date = interest_date + timedelta(days=days_to_monday)
        return interest_date


    """ METHODS """


    def improve(self) -> None:
        for i in range(500):
            self.mutate()

        print('done')
        # Switch.random(self.schedule)

    def mutate(self): # this will probably be a class one day...
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # pick a shift to replace
        shift_to_replace = random.choice(self.schedule)

        # calculate the cost and find what employee previously had that shift
        MC = MalusCalculator(self.schedule, self.db, self.cursor)
        old_cost = MC.get_wage_costs_per_week(self.schedule)
        old_employee = shift_to_replace[4]

        # get index of the choice so we can find what employees can work
        index = int(shift_to_replace[5])

        # use available_employees dict to pick from list with employees that can work that shift
        employee_for_shift = random.choice(self.available_employees[index])
        employee, wage = employee_for_shift

        # replace employee with new employee
        self.schedule[index][4] = employee
        new_cost = MC.get_wage_costs_per_week(self.schedule)

        # check if improvement worked, if not, place old employee back
        if new_cost['schedule'] > old_cost['schedule']:
            self.schedule[index][4] = old_employee
