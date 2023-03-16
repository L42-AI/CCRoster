<<<<<<< HEAD
import datetime
=======
from datetime import datetime
import numpy as np
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
import random

from classes.representation.dataclasses import Shift, Availability
from classes.representation.employee import Employee

from data.assign import employee_list, shift_list

OFFLINE = True # employee.id is downloaded form server, so when offline, use index of employee object in employeelist as id
class Generator:
    def __init__(self) -> None:
<<<<<<< HEAD
        self.shifts = shift_list # shift list from assign with shift instances
        self.employees = employee_list
        self.avalabilities = self.init_availability()
        self.workload = self.init_workload()
        self.schedule = self.init_schedule()
        self.id_employee = self.init_id_to_employee()
=======
        self.shift_list = shift_list # shift list from assign with shift instances
        self.employee_list = employee_list

        self.avalabilities = self.init_availabilities_list()
        self.workload = self.init_workload_dict()
        self.schedule = self.init_schedule_list()
        self.id_employee = self.init_id_to_employee_dict()
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
        self.improve()

    """ INIT """

<<<<<<< HEAD
    def init_availability(self) -> list[list[int, int]]:
        """
        Initiate the availability list, consists of tuples of id's and wages
        """

        availabilities: list[list[int, int]] = [self.__downloading_availabilities(shift) for shift in self.shifts]
        return availabilities

    def init_workload(self) -> dict:
        workload = {}
        for index, employee in enumerate(self.employees):

            # each employee will have a list with shift objects that correspond to the shifts he is scheduled for
            if OFFLINE:
                workload[index] = {}
            else:
                workload[employee.get_id()] = {}
        return workload

    def init_schedule(self) -> list[tuple[Shift, int]]:
        schedule: list[tuple[int, int]] = []

        for index in range(len(self.shifts)):

            # for the initialisation, place employee number 0 with wage 999
            schedule.append((888, 999))
        return schedule

    def init_id_to_employee(self) -> dict[int: Employee]:
=======
    """ Luka versie """
    """ Niet zeker of dit is wat je bedoelde, zo niet haal het lekker weg """
    def init_availabilities_list_luka(self) -> list[list[Employee]]:

        return [self.__find_available_employees_for(shift) for shift in shift_list]

    def __find_available_employees_for(self, shift: Shift) -> list[Employee]:
        available_employees = []

        for employee in employee_list:

            if self.__availability_between(employee, shift):
                available_employees.append(employee)

        return available_employees

    def __availability_between(self, employee: Employee, shift: Shift) -> bool:
        for availability in employee.availability:

            # Check for start and end of availability
            if shift.start > availability.start:
                return False
            elif shift.end < availability.end:
                return False
            else:
                return True


    def init_availabilities_list(self) -> list[list[int]]:
        """
        Initiate the availability list
        """

        availabilities = []

        # go over each shift and download the employees that can work that shift
        for shift in self.shift_list:
            available_employees = self.__downloading_availability_list(shift)
            availabilities.append(available_employees)

        return availabilities

    def init_workload_dict(self) -> dict[int: Shift]:
        workload = {}
        for index, employee in enumerate(self.employee_list):

            # each employee will have a list with shift objects that correspond to the shifts he is scheduled for
            if OFFLINE:
                workload[index] = []
            else:
                workload[employee.get_id()] = []
        return workload

    def init_schedule_list(self) -> list[tuple[Shift, int]]:
        schedule: list[tuple[int, int]] = []

        for index in range(len(self.shift_list)):

            # for the initialisation, place employee number 0 with wage 999
            employee_id = 888
            wage = 999
            schedule.append((employee_id, wage))
        return schedule

    def init_id_to_employee_dict(self) -> dict[int: Employee]:
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
        """
        returns dictionary that stores employees with their id as key
        """

        id_employee = {}
        if OFFLINE:
<<<<<<< HEAD
            for index, employee in enumerate(self.employees):
=======
            for index, employee in enumerate(self.employee_list):
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
                id_employee[index] = employee
        else:

            # when not offline, employees get their key as id
<<<<<<< HEAD
            for index, employee in enumerate(self.employees):
=======
            for index, employee in enumerate(self.employee_list):
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
                id_employee[employee.get_id()] = employee

        return id_employee
    """ METHODS """

<<<<<<< HEAD
    def __downloading_availabilities(self, shift: tuple[datetime.datetime, datetime.datetime, int]):
=======
    def __downloading_availability_list(self, shift: Shift) -> list[tuple[int, float]]:
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
        """"
        this method is only used to develop the generator, later, the info will actually be downlaoded
        for now it just returns a hardcoded list with availability
        """

<<<<<<< HEAD

        downloaded_availabilities = []
        for index, employee in enumerate(self.employees):
=======
        # shift in the format of availability data that employees have
        shift_info = (shift.start, shift.end, shift.task)

        downloaded_availabilities = []
        for index, employee in enumerate(self.employee_list):
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d

            # employee.availability is a list with Availability objects corresponding with datetimes they can work
            for workable_shift in employee.availability:

<<<<<<< HEAD
                if self.__possible_shift(workable_shift, employee, shift):
=======
                if (workable_shift.start, workable_shift.end, employee.get_tasks()) == shift_info:
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d

                    if OFFLINE:
                        # for now, use index as employee id since downloading the key from the server obviously does not work
                        downloaded_availabilities.append((index, employee.get_wage()))
                    else:
                        downloaded_availabilities.append((employee.get_id(), employee.get_wage()))
        return downloaded_availabilities

    def improve(self) -> None:
        for i in range(5000):
            self.mutate()

        print(self.schedule)


    def mutate(self): # this will probably be a class one day.......   One day....
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # pick a shift to replace
        shift_to_replace, index = self.__random_shift()

        # pick an employee that can work that shift
        possible_employee, wage = self.__random_employee(index)

        # get the duration of the shift
        minutes = self.__duration_in_minutes(shift_to_replace.start, shift_to_replace.end)

        # use minutes to calculate cost
        cost = self.__calculate_wage_with_minutes(minutes, wage)

        # check if costs are lower with this employee than previous\
        if cost < self.schedule[index][1]:

            # check if employee is not crossing weekly_max and place shift into workload
            if self.__workload(possible_employee, shift_to_replace.start):

                # add shift to workload dictionary
                self.schedule[index] = (shift_to_replace, possible_employee)
    """ Helper methods """

<<<<<<< HEAD
    def __possible_shift(self, workable_shift: Availability, employee: Employee, shift: Shift):

        if workable_shift.start < shift.start:
            return False
        if workable_shift.end > shift.end:
            return False
        if employee.get_tasks() != shift.task:
            return False
        return True

=======
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
    def __random_shift(self) -> tuple[tuple[int, int], int]:
        """
        returns a tuple with inside (1) a tuple containing shift info and (2) an index
        """

<<<<<<< HEAD
        index = random.randint(0, len(self.shifts) - 1)

        shift = self.shifts[index]
=======
        index = random.randint(0, len(self.shift_list) - 1)

        shift = self.shift_list[index]
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d

        return shift, index

    def __random_employee(self, index) -> tuple[int, int]:
        """
        returns a tuple with integers corresponding to an employee's id and wage
        """
        possible_employee = random.choice(self.avalabilities[index])

        return possible_employee

    def __duration_in_minutes(self, start, end) -> int:
        """
        returns the number of minutes in a shift using the start and end datetime objects
        """

        difference_in_minutes = (end - start).total_seconds() // 60  # difference in minutes

        return difference_in_minutes

    def __calculate_wage_with_minutes(self, minutes, wage) -> int:
        """
        returns the total wage using the amount of minutes to calculate it
        """

        wage_by_minute = wage / 60
        wage_cost = wage_by_minute * minutes
        return wage_cost

    def __workload(self, possible_employee, shift) -> bool:
        """
        returns True if the employee is allowed to work that shift given his/hers weekly max
        """

        self.__update_workload(possible_employee, shift, add=True)

        # get the week and check how many shift person is working that week
        weeknumber = shift.isocalendar()[1]

        # get possible employee object to check weekly max
        possible_employee_object = self.id_employee[possible_employee]


        if possible_employee_object.weekly_max[weeknumber] > len(self.workload[possible_employee][weeknumber]):

            return True

        # if person will not take on shift, delete it from workload
        self.__update_workload(possible_employee, shift)
        return False

    def __update_workload(self, possible_employee, shift, add=False):
        """
        updates workload dictionary when employee takes on new shift
        """
        # get the weeknumber of the shift
        weeknumber = shift.isocalendar()[1]

        if add:
            # add a shift to the workload of that employee that week
            if weeknumber not in self.workload[possible_employee]:

                self.workload[possible_employee] = {weeknumber:[shift]}

            else:
                self.workload[possible_employee][weeknumber].append(shift)

        else:
<<<<<<< HEAD
            self.workload[possible_employee][weeknumber].remove(shift)
=======
            self.workload[possible_employee][weeknumber].remove(shift)
>>>>>>> 1fd44bd519f620e10daa2cf00b701a995dbd0d7d
