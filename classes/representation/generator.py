import datetime
import random

from classes.representation.dataclasses import Shift, Availability
from classes.representation.employee import Employee

from data.assign import employee_list, shift_list

OFFLINE = True  # employee.id is downloaded from the server, so when offline, use index of employee object in employeelist as id

class Generator:
    def __init__(self) -> None:
        self.shifts = shift_list  # shift list from assign with shift instances
        self.employees = employee_list
        self.availabilities = self.init_availability()
        self.workload = self.init_workload()
        self.schedule = self.init_schedule()
        self.id_employee = self.init_id_to_employee()
        self.improve()

    """ INIT """

    def init_availability(self) -> list[list[Employee]]:
        """
        Initiate the availability list, consists of employee objects
        """

        availabilities: list[list[Employee]] = [self.__downloading_availabilities(shift) for shift in self.shifts]
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

    def init_schedule(self) -> list[tuple[Shift, Employee]]:
        schedule: list[tuple[Shift, Employee]] = []

        for index in range(len(self.shifts)):

            # for the initialisation, place a dummy employee with id -1 and wage 999
            dummy_employee = Employee("Dummy", "Employee", [], 999, 999, 1, "everything", 1)
            schedule.append((self.shifts[index], dummy_employee))
        return schedule

    def init_id_to_employee(self) -> dict[int, Employee]:
        """
        returns dictionary that stores employees with their id as key
        """

        id_employee = {}
        if OFFLINE:
            for index, employee in enumerate(self.employees):
                id_employee[index] = employee
        else:

            # when not offline, employees get their key as id
            for index, employee in enumerate(self.employees):
                id_employee[employee.get_id()] = employee

        return id_employee

    """ METHODS """

    def __downloading_availabilities(self, shift: Shift) -> list[Employee]:
        """
        this method is only used to develop the generator, later, the info will actually be downloaded
        for now it just returns a hardcoded list with availability
        """

        downloaded_availabilities = []
        for index, employee in enumerate(self.employees):

            # employee.availability is a list with Availability objects corresponding with datetimes they can work
            for workable_shift in employee.availability:

                if self.__possible_shift(workable_shift, employee, shift):

                    if OFFLINE:
                        # for now, use index as employee id since downloading the key from the server obviously does not work
                        downloaded_availabilities.append(employee)
                    else:
                        downloaded_availabilities.append(employee)
        return downloaded_availabilities

    def improve(self) -> None:
        for i in range(5000):
            self.mutate()

        print(self.schedule)

    
    def mutate(self):  # this will probably be a class one day...
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # pick a shift to replace
        shift_to_replace, index = self.__random_shift()

        # pick an employee that can work that shift
        possible_employee = self.__random_employee(index)  # Updated to get only the Employee object

        # get the duration of the shift
        minutes = self.__duration_in_minutes(shift_to_replace.start, shift_to_replace.end)

        # use minutes to calculate cost
        cost = self.__calculate_wage_with_minutes(minutes, possible_employee.get_wage())  # Access the wage directly

        # check if costs are lower with this employee than previous
        if cost < self.schedule[index][1].get_wage():

            # check if employee is not crossing weekly_max and place shift into workload
            if self.__workload(possible_employee, shift_to_replace.start):

                # add shift to workload dictionary
                self.schedule[index] = (shift_to_replace, possible_employee)
    """ Helper methods """

    def __possible_shift(self, workable_shift: Availability, employee: Employee, shift: Shift):

        if workable_shift.start < shift.start:
            return False
        if workable_shift.end > shift.end:
            return False
        if employee.get_tasks() != shift.task:
            return False
        return True

    def __random_shift(self) -> tuple[tuple[int, int], int]:
        """
        returns a tuple with inside (1) a tuple containing shift info and (2) an index
        """

        index = random.randint(0, len(self.shifts) - 1)

        shift = self.shifts[index]

        return shift, index

    def __random_employee(self, index) -> Employee:
        """
        returns an Employee object
        """
        possible_employee = random.choice(self.availabilities[index])

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

    def __workload(self, possible_employee: Employee, shift: datetime.datetime) -> bool:
        """
        returns True if the employee is allowed to work that shift given his/hers weekly max
        """

        employee_key = possible_employee.get_id() if not OFFLINE else self.employees.index(possible_employee)
        self.__update_workload(employee_key, shift, add=True)

        # get the week and check how many shifts the person is working that week
        weeknumber = shift.isocalendar()[1]

        if possible_employee.get_week_max(weeknumber) > len(self.workload[employee_key][weeknumber]):
            return True

        # if the person will not take on the shift, delete it from the workload
        self.__update_workload(employee_key, shift)
        return False

    def __update_workload(self, employee_key: int, shift: datetime.datetime, add=False):
        """
        updates workload dictionary when an employee takes on a new shift
        """
        # get the week number of the shift
        weeknumber = shift.isocalendar()[1]

        if add:
            # add a shift to the workload of that employee that week
            if weeknumber not in self.workload[employee_key]:
                self.workload[employee_key] = {weeknumber: [shift]}
            else:
                self.workload[employee_key][weeknumber].append(shift)
        else:
            self.workload[employee_key][weeknumber].remove(shift)