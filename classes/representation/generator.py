import numpy as np
from datetime import date
from datetime import timedelta
from tqdm import tqdm
from data.assign import employee_list



SCHEDULE_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DAILY_SHIFTS = ['730 - 1200', '1200 - 1730']
EMPLYEE_PER_SHIFT = 1

class Generator:
    def __init__(self) -> None:
        self.employee_list = employee_list
        self.schedule = self.init_schedule()
        print(self.schedule)
        self.fill_schedule()
        print(self.schedule)


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

        # Set start date
        start_date = self.get_date()

        # Set day increase for increasing day count
        day_increase = timedelta(1)

        # Set start day
        start_day = self.get_day(start_date)

        # Find start date which must be a monday
        # Start of the schdedule
        while start_day != 'Monday':
            start_date = start_date + day_increase
            start_day = self.get_day(start_date)

        return start_date

    def get_end_day(self) -> object:
        """
        Find date of end of schedule
        """

        # Set end date
        end_date = self.get_date()

        # Set starting month
        start_month = end_date.month

        # Set day increase for increasing day count
        day_increase = timedelta(1)

        # Set end day
        end_day = self.get_day(end_date)

        # Find end date which must be a monday
        # End of the schdedule is the day before monday
        # Month must be one further than start month
        while end_day != 'Monday' or end_date.month != start_month + 1:
            end_date = end_date + day_increase
            end_day = self.get_day(end_date)

        return end_date

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


                if len(self.schedule[av_week][av_day][av_shift]) == EMPLYEE_PER_SHIFT:
                    fail_count += 1
                    continue
                else:
                    self.schedule[av_week][av_day][av_shift].append(name)
                    continue