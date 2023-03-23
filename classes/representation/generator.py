from datetime import datetime
import random

from classes.representation.dataclasses import Shift, Availability
from classes.representation.employee import Employee
from classes.representation.malus_calc import MalusCalc
from classes.representation.greedy import Greedy


from data.assign import employee_list, shift_list

OFFLINE = True  # employee.id is downloaded from the server, so when offline, use index of employee object in employeelist as id

class Generator:
    def __init__(self) -> None:
        self.shifts = shift_list  # shift list from assign with shift instances
        self.employees = employee_list
        self.init_employees_id_offline()
        self.init_shifts_id_offline()

        self.id_employee = self.init_id_to_employee()
        self.id_shift = self.init_id_to_shift()
        self.id_wage = self.init_id_to_wage()
        self.time_conflict_dict = self.init_shifts_with_same_time()

        self.availabilities = self.init_availability()
        self.workload = self.init_workload()

        self.schedule = self.init_schedule()

        # Greedy fill methods
        # self.schedule = Greedy.fill_employees(self.schedule, self.employees)
        self.schedule = Greedy.fill_shifts(self.schedule, self.shifts, self.availabilities)

        print(self.schedule)

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

    def init_shifts_id_offline(self):
        """
        temporary method to assign id's to shifts
        """
        for id, shift in enumerate(self.shifts):
            shift.id = id

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

    def init_workload(self) -> dict[int, dict[int, list[int]]]:
        return {employee.get_id() : {} for employee in self.employees}

    def init_schedule(self) -> list[tuple[int, None]]:
        return [(shift.get_id(), None) for shift in self.shifts]

    def init_shifts_with_same_time(self) -> dict[int, set[int]]:
        time_conflict_dict = {}
        for shift_1 in self.shifts:
            time_conflict_dict[shift_1.get_id()] = set()
            for shift_2 in self.shifts:
                if shift_1 is shift_2:
                    continue
                if shift_1.start <= shift_2.start <= shift_1.end <= shift_2.end >= shift_1.start:
                    time_conflict_dict[shift_1.get_id()].add(shift_2.get_id())
                elif shift_1.start >= shift_2.start <= shift_1.end >= shift_2.end >= shift_1.start:
                    time_conflict_dict[shift_1.get_id()].add(shift_2.get_id())
                elif shift_1.start >= shift_2.start <= shift_1.end <= shift_2.end >= shift_1.start:
                    time_conflict_dict[shift_1.get_id()].add(shift_2.get_id())
                elif shift_1.start <= shift_2.start <= shift_1.end >= shift_2.end >= shift_1.start:
                    time_conflict_dict[shift_1.get_id()].add(shift_2.get_id())
        return time_conflict_dict

    """ GET """

    def get_shift(self, id: int) -> Shift:
        return self.id_shift.get(id)

    def get_employee(self, id: int) -> Employee:
        return self.id_employee.get(id)

    def get_workload(self, id: int) -> dict[int, list]:
        return self.workload.get(id)
    
    def get_weeknumber(self, shift_id: int) -> int:
        shift_obj = self.get_shift(shift_id)
        return shift_obj.start.isocalendar()[1]

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

    def get_colliding_shifts(self, shift_id: int) -> set[int]:
        return self.time_conflict_dict.get(shift_id)


    """ METHODS """

    def improve(self) -> None:
        for i in range(200):
            self.mutate()

    def print_schedule(self) -> None:
        # Format and print the schedule
        for i, info in enumerate(self.schedule):
            shift_id, employee_id = info
            print(shift_id, employee_id)

        self.total_costs = self.wage_cost()
        print(self.total_costs)

    def wage_cost(self) -> int:
        total_cost = 0
        for shift_id, employee_id in self.schedule:
            shift = self.get_shift(shift_id)
            employee = self.get_employee(employee_id)
            cost = shift.duration * employee.get_wage()
            total_cost += cost
        return total_cost

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
        shift_duration_hours = shift_to_replace.duration

        # use hours to calculate cost
        new_cost = self.__compute_cost(shift_duration_hours, possible_employee_id, shift_to_replace.get_id())  # Access the wage directly

        # check if costs are lower with this employee than previous
        shift_id, current_employee_id = self.schedule[index]
        current_employee_obj = self.get_employee(current_employee_id)
        shift_obj = self.get_shift(shift_id)
        current_cost = current_employee_obj.wage * shift_obj.duration

        if new_cost < current_cost:

            # check if employee is not crossing weekly_max and place shift into workload
            if self.__workload(possible_employee_id, shift_to_replace.get_id()):

                # add shift to workload dictionary
                if self.passed_hard_constraints(index):
                    self.schedule[index] = (shift_to_replace.get_id(), possible_employee_id)

    """ HARD CONSTRAINTS """

    def passed_hard_constraints(self, index: int) -> bool:
        if not self.same_time(index):
            return False
        print('passed')
        return True


    def same_time(self, index: int) -> bool:
        shift_id, employee_id = self.schedule[index]

        if employee_id is None:
            raise ValueError('No employee in the schedule')

        colliding_shifts = self.get_colliding_shifts(shift_id)
        for colliding_shift_id in colliding_shifts:
            if self.schedule[colliding_shift_id][1] == employee_id:
                return False
        
        return True
        

    def same_day(self, index: int) -> bool:
        shift_id, employee_id = self.schedule[index]
    
        if employee_id is None:
            return False
        
        shift = self.get_shift(shift_id)
        employee = self.get_employee(employee_id)

        employee
    
        shift_start_day = shift.start.day
        shift_start_hour = shift.start.hour
        shift_start_minute = shift.start.minute
    
        shift_end_day = shift.end.day
        shift_end_hour = shift.end.hour
        shift_end_minute = shift.end.minute

        for i, match_shift in enumerate(self.shifts):
            if match_shift.start.day == shift_start_day and shift != match_shift:
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

    def __compute_cost(self, hours: float, possible_employee_id: int, shift_id: int) -> float:
        """
        returns the total pay using the wage and shift in hours. Also takes into account that if an employee has a
        weekly min, the first shifts are 'free'
        """

        possible_employee_object = self.get_employee(possible_employee_id)
        employee_shifts = self.get_workload(possible_employee_id)
        weeknumber = self.get_weeknumber(shift_id)
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

    def __workload(self, possible_employee_id: int, shift_id: int) -> bool:
        """
        returns True if the employee is allowed to work that shift given his/hers weekly max
        """

        possible_employee_object = self.get_employee(possible_employee_id)

        self.__update_workload(possible_employee_id, shift_id, add=True)

        # get the week and check how many shifts the person is working that week
        weeknumber = self.get_weeknumber(shift_id)

        if possible_employee_object.get_week_max(weeknumber) > len(self.workload[possible_employee_id][weeknumber]):
            return True
        else:
            # if the person will not take on the shift, delete it from the workload
            self.__update_workload(possible_employee_id, shift_id)
            return False

    def __update_workload(self, employee_id: int, shift_id: int, add=False) -> None:
        """
        updates workload dictionary when an employee takes on a new shift
        """
        # get the week number of the shift
        weeknumber = self.get_weeknumber(shift_id)

        if weeknumber not in self.workload[employee_id]:
            self.workload[employee_id] = {weeknumber: []}

        if add:
            # add a shift to the workload of that employee that week
            self.workload[employee_id][weeknumber].append(shift_id)
        else:
            self.workload[employee_id][weeknumber].remove(shift_id)