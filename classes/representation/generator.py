from datetime import date, timedelta
import numpy as np
import random
import mysql.connector

from classes.representation.maluscalc import MalusCalculator
from classes.algorithms.switch import Switch
from classes.representation.GUI_output import SCHEDULE_DAYS, DAILY_SHIFTS, EMPLOYEE_PER_SHIFT
from data.assign import employee_list

class Generator:
    def __init__(self) -> None:
        self.employee_list = employee_list
        self.schedule = self.init_schedule()
        self.fill_schedule()
        print(self.schedule)
        self.improve()
        self.db = mysql.connector.connect(
            host="185.224.91.162",
            port=3308,
            user="Jacob",
            password="wouterisdebestehuisgenoot",
            database="rooster" # niet veranderen
        )
        self.cursor = self.db.cursor()
    """ INIT """

    def init_schedule(self) -> object:
        """
        Initiate the schedule
        """

        # Set the start and end day for the schedule
        start_date = self.get_start_day()
        end_date = self.get_end_day()

        # Calculate the amount of days to be scheduled
        scheduling_days = (end_date - start_date).days

        # Set the amount of weeks, days and shifts to be scheduled
        weeks = scheduling_days // len(SCHEDULE_DAYS)
        days = len(SCHEDULE_DAYS)
        shifts = len(DAILY_SHIFTS)

        # Create schedule
        schedule = np.empty((weeks, days, shifts), dtype=list)

        # Fill schedule with empty lists
        # So that more employees can work during the same shift
        for week_num, week in enumerate(schedule):
            for day_num, day in enumerate(week):
                for shift_num in range(len(day)):
                    schedule[week_num][day_num][shift_num] = []

        return schedule

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