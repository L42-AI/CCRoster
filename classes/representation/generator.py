from datetime import *
import numpy as np
import random

from classes.representation.maluscalc import MalusCalculator
from data.assign import *
class Generator:
    def __init__(self) -> None:
        self.shifts: list[tuple] = shift_list # shift list from assign with shift instances
        self.avalabilities: list[list] = self.init_availability()
        self.work_load: dict = self.init_work_load()
        self.schedule: list[tuple[int, int]] = self.init_schedule()
        self.improve()


    """ INIT """

    def init_availability(self) -> list[list]:
        """
        Initiate the availability list
        """

        availabilities: list[list[int]] = []

        # go over each shift and download the employees that can work that shift
        for shift in self.shifts:
            available_employees = self.__downloading_availabilities(shift)
            availabilities.append(available_employees)

        return availabilities

    def init_work_load(self) -> dict:
        work_load = {}
        for employee in employee_list:

            # each employee will have a list with shift objects that correspond to the shifts he is scheduled for
            work_load[employee.get_id()] = []

        return work_load

    def init_schedule(self) -> list[tuple[int, int]]:
        schedule: list[tuple[int, int]] = []

        for index in range(len(self.shifts)):

            # for the initialisation, place employee number 0 with wage 999
            schedule.append((0, 999))
        return schedule

    """ METHODS """

    def __downloading_availabilities(self, shift: tuple[datetime, datetime, int]):
        """"
        this method is only used to develop the generator, later, the info will actually be downlaoded
        for now it just returns a hardcoded list with availability
        """

        # shift in the format of availability data that employees have
        shift_info = (shift.start, shift.end, shift.task)

        downloaded_availabilities = []
        for index, employee in enumerate(employee_list):

            # employee.availability is a list with Availability objects corresponding with datetimes they can work
            for workable_shift in employee.availability:

                if (workable_shift.start, workable_shift.end, employee.get_tasks()) == shift_info:

                    # for now, use index as employee id since downloading the key from the server obviously does not work
                    downloaded_availabilities.append((index + 1, employee.get_wage()))

        return downloaded_availabilities

    def improve(self) -> None:
        for i in range(500):
            self.mutate()

        print('done')


    def mutate(self): # this will probably be a class one day...
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # pick a shift to replace
        shift_to_replace, index = self.__random_shift()

        # pick an employee that can work that shift
        possible_employee = self.__random_employee(index)

        # get the duration of the shift
        minutes = self.__duration_in_minutes(shift_to_replace.start, shift_to_replace.end)
        # print(possible_employee)

        # # calculate the cost and find what employee previously had that shift
        # MC = MalusCalculator(self.schedule, self.db, self.cursor)
        # old_cost = MC.get_wage_costs_per_week(self.schedule)
        # old_employee = shift_to_replace[4]

        # # get index of the choice so we can find what employees can work
        # index = int(shift_to_replace[5])

        # # use available_employees dict to pick from list with employees that can work that shift
        # employee_for_shift = random.choice(self.available_employees[index])
        # employee, wage = employee_for_shift

        # # replace employee with new employee
        # self.schedule[index][4] = employee
        # new_cost = MC.get_wage_costs_per_week(self.schedule)

        # # check if improvement worked, if not, place old employee back
        # if new_cost['schedule'] > old_cost['schedule']:
        #     self.schedule[index][4] = old_employee

    def __random_shift(self) -> tuple[tuple[int, int], int]:
        """
        returns a tuple with inside (1) a tuple containing shift info and (2) an index
        """
        # print(self.shifts[0])
        index = random.randint(0, len(self.shifts) - 1)
        # print(index)
        shift = self.shifts[index]
        return shift, index

    def __random_employee(self, index) -> tuple[int, int]:
        """
        returns a tuple with integers corresponding to an employee's id and wage
        """
        id_wage = random.choice(self.avalabilities[index])
        return id_wage

    def __duration_in_minutes(self, start, end) -> int:

        difference_in_minutes = (end - start).total_seconds() // 60  # difference in minutes

        print(difference_in_minutes)
        raise