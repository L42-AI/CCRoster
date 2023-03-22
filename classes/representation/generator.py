from datetime import datetime
import random

from classes.representation.dataclasses import Shift, Availability
from classes.representation.employee import Employee
from classes.representation.malus_calc import MalusCalc

from data.assign import employee_list, shift_list

OFFLINE = True  # employee.id is downloaded from the server, so when offline, use index of employee object in employeelist as id

class Generator:
    def __init__(self) -> None:
        self.shifts = shift_list  # shift list from assign with shift instances
        self.employees = employee_list

        self.id_employee = self.init_id_to_employee()
        self.id_shift = self.init_id_to_shift()

        self.availabilities = self.init_availability()
        self.workload = self.init_workload()
        self.schedule = self.init_schedule_empty()
        self.fill_schedule_based_on_shifts()
        # self.improve()
        self.print_schedule()
        # print(f'Wage cost = €{self.get_wage()}')

    """ INIT """


    def init_id_to_employee(self) -> dict[str, Employee]:
        """
        returns dictionary that stores employees with their id as key
        """
        return {employee.get_id(): employee for employee in self.employees}

    def init_id_to_shift(self) -> dict[str, Shift]:
        """
        returns dictionary that stores employees with their id as key
        """
        return {shift.get_id(): shift for shift in self.shifts}

    def get_shift(self, id: str) -> Shift:
        return self.id_shift.get(id)

    def get_employee(self, id: str) -> Employee:
        return self.id_employee.get(id)

    def init_schedule_empty(self) -> list[tuple[str, None]]:
        return [(shift.get_id(), None) for shift in self.shifts]

    def fill_schedule_based_on_employees(self) -> None:
        # Sort on availability to first do people with little availability
        sorted_employees = sorted(self.employees, key=lambda employee: len(employee.availability))
        
        for i, employee in enumerate(sorted_employees):
            shift_id = self.schedule[i][0]
            self.schedule[i] = (shift_id, employee.get_id())

    def fill_schedule_based_on_shifts(self) -> None:

        indexes_list = [i for i in range(len(self.shifts))]
        sorted_index = sorted(indexes_list, key = lambda i: len(self.availabilities[i]))

        for index in sorted_index:
            for i, tuple_info in enumerate(self.schedule):
                shift = self.get_shift(tuple_info[0])
                if shift is self.shifts[index]:
                    random_employee = self.__get_random_employee(index)
                    self.schedule[i] = (shift.get_id(), random_employee.get_id())

    def fill_schedule_based_on_shifts(self) -> None:

        shift_availability_dict: dict[Shift.id: list[Employee.id]] = {}
        self.schedule: dict[Shift.id: Employee.id] = {}

        sorted_dict = dict(sorted(shift_availability_dict.items(), key=lambda x: len(shift_availability_dict[x])))

        for shift_id in sorted_dict:
            self.schedule[shift_id] = self.__get_random_employee(shift_id)

    def init_availability(self) -> list[list[Employee]]:
        """
        Initiate the availability list, consists of employee objects
        """

        availabilities: list[list[Employee]] = [self.downloading_availabilities(shift) for shift in self.shifts]
        return availabilities

    def init_workload(self) -> dict[str, dict]:
        return {employee.get_id() : {} for employee in self.employees}

    def init_schedule(self) -> list[tuple[Shift, Employee]]:
        schedule: list[tuple[Shift, Employee]] = []

        for i, shift in enumerate(self.shifts):

            # for the initialisation, place a dummy employee with id -1 and wage 999
            dummy_employee = Employee("Dummy", "Employee", [], 999, 999, 1, "Allround", 1)
            schedule.append((shift, dummy_employee))
        return schedule

    """ METHODS """

    def downloading_availabilities(self, shift: Shift) -> list[Employee]:
        """
        this method is only used to develop the generator, later, the info will actually be downloaded
        for now it just returns a hardcoded list with availability
        """


        """ Deze method heeft nog wat dubbele code """
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
        for i in range(len(self.schedule)):
            self.mutate()

    def print_schedule(self) -> None:
        # Format and print the schedule
        for i, info in enumerate(self.schedule):
            shift_id, employee_id = info
            self.passed_hard_constraints(i)
            print(f"{self.get_shift(shift_id)} - {self.get_employee(employee_id)}")


    def get_wage(self) -> float:
        wage_cost = MalusCalc.wage_cost(self.schedule)
        return wage_cost

    def mutate(self):  # this will probably be a class one day...
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # pick a shift to replace
        shift_to_replace, index = self.__get_random_shift()

        # pick an employee that can work that shift
        possible_employee = self.__get_random_employee(index)  # Updated to get only the Employee object

        # get the duration of the shift
        shift_duration_hours = self.__get_duration_in_hours(shift_to_replace.start, shift_to_replace.end)

        # use hours to calculate cost
        new_cost = self.__compute_cost(shift_duration_hours, possible_employee.get_wage())  # Access the wage directly

        # check if costs are lower with this employee than previous
        current_cost = self.schedule[index][1].get_wage()
        if new_cost < current_cost:

            # check if employee is not crossing weekly_max and place shift into workload
            if self.__workload(possible_employee, shift_to_replace.start):

                # add shift to workload dictionary
                self.schedule[index] = (shift_to_replace, possible_employee)

    """ HARD CONSTRAINTS """

    def passed_hard_constraints(self, index: int) -> bool:
        if not self.same_day(index):
            return False
        print('yes')

    def same_day(self, index: int) -> bool:
        shift_id, employee_id = self.schedule[index]
        if employee_id is None:
            return False
        shift = self.get_shift(shift_id)
        shift_day = shift.start.day
        for i, match_shift in enumerate(self.shifts):
            if match_shift.start.day == shift_day and shift != match_shift:
                if employee_id == self.schedule[i][1]:
                    return False
        return True


    """ Helper methods """

    def __possible_shift(self, workable_shift: Availability, employee: Employee, shift: Shift) -> bool:

        # Check time
        if workable_shift.start > shift.start or workable_shift.end < shift.end:
            return False

        # Check task
        tasks_list = employee.get_tasks()
        for task in tasks_list:
            if task == shift.task:
                return True
        return False

    def __get_random_shift(self) -> tuple[Shift, int]:
        """
        returns a tuple with inside (1) a tuple containing shift info and (2) an index
        """

        index = random.randint(0, len(self.shifts) - 1)

        shift = self.shifts[index]

        return shift, index

    def __get_random_employee(self, index) -> Employee:
        """
        returns an Employee object
        """
        return random.choice(self.availabilities[index])

    def __get_duration_in_hours(self, start: datetime, end: datetime) -> float:
        """
        returns the number of hours in a shift using the start and end datetime objects
        """
        return (end - start).total_seconds() / 3600  # difference in hours

    def __compute_cost(self, hours: float, hourly_wage: int) -> float:
        """
        returns the total pay using the wage and shift in hours
        """
        return hourly_wage * hours # Multiply duration with hourly wage to get total pay

    def __workload(self, possible_employee: Employee, shift: datetime) -> bool:
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

    def __update_workload(self, employee_key: int, shift: datetime, add=False) -> None:
        """
        updates workload dictionary when an employee takes on a new shift
        """
        # get the week number of the shift
        weeknumber = shift.isocalendar()[1]

        if weeknumber not in self.workload[employee_key]:
            self.workload[employee_key] = {weeknumber: []}

        if add:
            # add a shift to the workload of that employee that week
            self.workload[employee_key][weeknumber].append(shift)
        else:
            self.workload[employee_key][weeknumber].remove(shift)