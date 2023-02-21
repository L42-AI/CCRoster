from datetime import date, timedelta
import numpy as np
import random
import mysql.connector

from classes.representation.maluscalc import MalusCalculator
from classes.algorithms.switch import Switch
from classes.representation.GUI_output import SCHEDULE_DAYS, DAILY_SHIFTS, EMPLOYEE_PER_SHIFT
from data.assign import employee_list
from data.queries import *

class Generator:
    def __init__(self) -> None:
        self.db, self.cursor = db_cursor()
        self.employee_list = employee_list
        self.available_employees = [] # list with all employees that can work the shift with the same index in schedule
        self.schedule = self.init_schedule() # array with shifts that need to be filled
        self.availability = self.init_availability() # array with all shifts that each employee can fill
        # self.fill_schedule()
        print(self.available_employees)
        self.improve()
    """ INIT """

    def init_schedule(self) -> object:
        """
        Initiate the schedule
        """

        # get list of tuples of shifts needed
        shifts_needed = downloading_shifts(self.db, self.cursor)
        schedule = np.zeros((len(shifts_needed), 5))

        # transfer to np.array
        days = set()
        shift = 0
        queries_list = []
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
            ## week, day, shift, task, employee_id
            schedule[_] = (week, day, shift, task, 0)

            # collect all employees that can work this shift
            self.available_employees.append(employee_per_shift(self.db, self.cursor, schedule[_]))

        return schedule

    def init_availability(self):
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

    def fill_schedule(self) -> None:
        """
        Method to fill the schedule
        """

        # Make set to track amount of filled timeslots
        filled_schedule_set = set()
        failcounter = 0

        # While set is not length of filled schedule
        while len(filled_schedule_set) < len(DAILY_SHIFTS) * len(SCHEDULE_DAYS) * 4:

            # Reset schedule if too many failed tries
            if failcounter > 100000:
                self.schedule = self.init_schedule()
                failcounter = 0

            # Get employee name and availability
            employee = random.choice(self.employee_list)
            name = employee.get_name()
            availability_code = employee.get_av()

            # Skip if no availability
            if availability_code == None:
                continue

            # Unpack code for indexing
            av_week = availability_code[0]
            av_day = availability_code[1]
            av_shift = availability_code[2]

            # If slot in schedule is full
            if len(self.schedule[av_week][av_day][av_shift]) == EMPLOYEE_PER_SHIFT:
                filled_schedule_set.add((av_week, av_day, av_shift))
                failcounter += 1
                continue
            else:
                self.schedule[av_week][av_day][av_shift].append(name)
                continue

    def improve(self) -> None:
        MC = MalusCalculator(self.schedule)
        MC.calc_malus()
        Switch.random(self.schedule)