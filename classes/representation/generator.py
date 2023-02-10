import numpy as np
from datetime import date
from datetime import timedelta
from data.assign import employee_list
from classes.representation.maluscalc import MalusCalculator



SCHEDULE_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DAILY_SHIFTS = ['730 - 1200', '1200 - 1730']
EMPLOYEE_PER_SHIFT = 1

class Generator:
    def __init__(self) -> None:
        self.employee_list = employee_list
        self.schedule = self.init_schedule()
        self.fill_schedule()
        self.improve()



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
        Find date of start of schedule
        """
        return self.get_schedule_boundary(start=True)

    def get_end_day(self) -> object:
        """
        Find date of end of schedule
        """
        return self.get_schedule_boundary(start=False)

    def get_schedule_boundary(self, start) -> object:
        """
        Find date of start or end of schedule
        """

        # Set start or end date
        schedule_date = self.get_date()

        # Set starting month
        start_month = schedule_date.month

        # Set day increase for increasing day count
        day_increase = timedelta(1)

        # Set schedule day
        schedule_day = self.get_day(schedule_date)

        # Find start or end date
        # Start of the schdedule: a Monday
        # End of the schdedule: day before Monday and in next month
        while schedule_day != 'Monday' or (not start and schedule_date.month != start_month + 1):
            schedule_date = schedule_date + day_increase
            schedule_day = self.get_day(schedule_date)

        return schedule_date


    """ METHODS """

    def fill_schedule(self) -> None:
        """
        Method to fill the schedule
        """


        fail_count = 0
        while fail_count <= 100000:
            for employee in self.employee_list:
                name = employee.get_name()
                availability_code = employee.get_av()
                av_week = availability_code[0]
                av_day = availability_code[1]
                av_shift = availability_code[2]

                if len(self.schedule[av_week][av_day][av_shift]) == EMPLOYEE_PER_SHIFT:
                    fail_count += 1
                    continue
                else:
                    self.schedule[av_week][av_day][av_shift].append(name)
                    continue

    def improve(self) -> None:
        MC = MalusCalculator(self.schedule)
        MC.calc_malus()