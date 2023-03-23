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
        self.init_employees_id_offline()

        self.id_employee = self.init_id_to_employee()
        self.id_shift = self.init_id_to_shift()
        self.id_wage = self.init_id_to_wage()

        self.availabilities = self.init_availability()
        self.workload = self.init_workload()

        self.schedule = self.init_schedule_empty()
        self.fill_schedule_based_on_shifts()
        self.improve()
        self.print_schedule()
        # print(f'Wage cost = €{self.get_wage()}')

    """ INIT DATA STRUCTURES """

    def init_employees_id_offline(self):
        """
        temporary method to assign id's to employees
        """
        for id, employee in enumerate(self.employees):
            employee.id = id

    def init_id_to_employee(self) -> dict[int, Employee]:
        """
        returns dictionary that stores employees with their id as key
        """
        return {employee.get_id(): employee for employee in self.employees}

    def init_id_to_shift(self) -> dict[int, Shift]:
        """
        returns dictionary that stores employees with their id as key
        """
        return {shift.get_id(): shift for shift in self.shifts}

    def init_id_to_wage(self) -> dict[int, float]:
        return {employee.get_id(): employee.get_wage() for employee in self.employees}

    def init_availability(self) -> list[list[int]]:
        """
        Initiate the availability list, consists of employee objects
        """
        return [self.get_employee_list(shift) for shift in self.shifts]

    def init_workload(self) -> dict[int, dict[int, list]]:
        return {employee.get_id() : {} for employee in self.employees}


    """ GET """

    def get_shift(self, id: int) -> Shift:
        return self.id_shift.get(id)

    def get_employee(self, id: int) -> Employee:
        return self.id_employee.get(id)

    def get_workload(self, id: int) -> dict[int, list]:
        return self.workload.get(id)
    
    def get_weeknumber(self, moment: datetime) -> int:
        return moment.isocalendar()[1]

    def get_employee_list(self, shift: Shift) -> list[int]:
        """
        this method is only used to develop the generator, later, the info will actually be downloaded
        for now it just returns a hardcoded list with availability
        """

        downloaded_availabilities = []
        for employee in self.employees:

            # employee.availability is a list with Availability objects corresponding with datetimes they can work
            for workable_shift in employee.availability:

                if self.__possible_shift(workable_shift, employee, shift):
                    downloaded_availabilities.append(employee.get_id())

        return downloaded_availabilities

    """ SCHEDULE """

    def init_schedule_empty(self) -> list[tuple[int, None]]:
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
            random_employee = self.__get_random_employee(index)
            wage = self.id_wage[random_employee]
            self.schedule[index] = (self.shifts[index], random_employee, wage)


    """ DEZE WORDT NIET GEBUIKT, KAN WEG? """
    def init_schedule(self) -> list[tuple[Shift, Employee]]:
        schedule: list[tuple[Shift, Employee]] = []

        for i, shift in enumerate(self.shifts):

            # for the initialisation, place a dummy employee with id -1 and wage 999
            dummy_employee = Employee("Dummy", "Employee", [], 999, 999, 1, "Allround", 1)
            schedule.append((shift, dummy_employee, 999))
        return schedule

    """ METHODS """

    def improve(self) -> None:
        for i in range(200):
            self.mutate()

    def print_schedule(self) -> None:
        # Format and print the schedule
        for i, info in enumerate(self.schedule):
            shift_id, employee_id, wage = info
            # self.passed_hard_constraints(i)
            print(shift_id, employee_id, wage)

        self.total_costs = MalusCalc.total_costs(self.schedule, self.employees)
        print(self.total_costs)

    def mutate(self):  # this will probably be a class one day...
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # pick a shift to replace
        shift_to_replace, index = self.__get_random_shift()

        # pick an employee that can work that shift
        possible_employee_id = self.__get_random_employee(index)  # Updated to get only the Employee object

        # get the duration of the shift
        shift_duration_hours = self.__get_duration_in_hours(shift_to_replace.start, shift_to_replace.end)

        # use hours to calculate cost
        new_cost = self.__compute_cost(shift_duration_hours, possible_employee_id, shift_to_replace.start)  # Access the wage directly

        # check if costs are lower with this employee than previous
        current_cost = self.schedule[index][2]
        if new_cost < current_cost:

            # check if employee is not crossing weekly_max and place shift into workload
            if self.__workload(possible_employee_id, shift_to_replace.start):

                # add shift to workload dictionary
                self.schedule[index] = (shift_to_replace, possible_employee_id, new_cost)

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

    def __get_random_employee(self, index) -> int:
        """
        returns an employee id
        """
        return random.choice(self.availabilities[index])

    def __get_duration_in_hours(self, start: datetime, end: datetime) -> float:
        """
        returns the number of hours in a shift using the start and end datetime objects
        """
        return (end - start).total_seconds() / 3600  # difference in hours

    def __compute_cost(self, hours: float, possible_employee_id: int, shift: datetime) -> float:
        """
        returns the total pay using the wage and shift in hours. Also takes into account that if an employee has a
        weekly min, the first shifts are 'free'
        """

        possible_employee_object = self.get_employee(possible_employee_id)
        employee_shifts = self.get_workload(possible_employee_id)
        weeknumber = self.get_weeknumber(shift)
        weekly_min = possible_employee_object.get_week_min(weeknumber)
        wage = possible_employee_object.get_wage()

        # if week not in workload, number of shifts that week == 0
        if weeknumber not in employee_shifts and weekly_min > 0:

            # this shift the worker works for 'free'
            return 0

        # check if worker is under his/hers weely min
        elif len(employee_shifts[weeknumber]) < weekly_min:
            return 0

        else:
            # if weekly_min is reached, calculate the wage it will cost normal way
            return wage * hours # Multiply duration with hourly wage to get total pay

    def __workload(self, possible_employee_id: int, shift_moment: datetime) -> bool:
        """
        returns True if the employee is allowed to work that shift given his/hers weekly max
        """

        possible_employee_object = self.get_employee(possible_employee_id)
        possible_employee_workload = self.get_workload(possible_employee_id)
        
        self.__update_workload(possible_employee_id, shift_moment, add=True)

        # get the week and check how many shifts the person is working that week
        weeknumber = self.get_weeknumber(shift_moment)

        if possible_employee_object.get_week_max(weeknumber) > len(possible_employee_workload[weeknumber]):
            return True
        else:
            # if the person will not take on the shift, delete it from the workload
            self.__update_workload(possible_employee_id, shift_moment)
            return False

    def __update_workload(self, employee_id: int, shift: datetime, add=False) -> None:
        """
        updates workload dictionary when an employee takes on a new shift
        """
        # get the week number of the shift
        weeknumber = self.get_weeknumber(shift)
        employee_workload = self.get_workload(employee_id)

        if weeknumber not in employee_workload:
            employee_workload = {weeknumber: []}

        if add:
            # add a shift to the workload of that employee that week
            employee_workload[weeknumber].append(shift)
        else:
            employee_workload[weeknumber].remove(shift)