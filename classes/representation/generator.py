from datetime import datetime, timedelta
import random
import copy

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
        self.update_highest_priority_list()

        self.id_employee = {
            employee.get_id(): employee for employee in self.employees}
        self.id_shift = {shift.get_id(): shift for shift in self.shifts}
        self.id_wage = {employee.get_id(): employee.get_wage()
                        for employee in self.employees}
        self.time_conflict_dict = self.init_coliding_dict()

        self.availabilities = {shift.id: self.get_employee_list(shift) for shift in self.shifts}
        self.actual_availabilities = {shift_id: [0, set(self.availabilities[shift_id])] for shift_id in self.availabilities}

        self.workload = self.init_workload()
        self.schedule = {shift.id: None for shift in self.shifts}

        self.greedy_fill()
        # self.random_fill()

        # print(self.compute_replacement_factor(self.actual_availabilities))

        # self.print_schedule()

        self.improve()
        self.total_costs = self.compute_wage_cost(self.schedule) + self.standard_cost(self.employees)
        # print(f'Wage cost = €{self.get_wage()}')

    """ INIT DATA STRUCTURES """

    def init_employees_id_offline(self) -> None:
        """
        temporary method to assign id's to employees
        """
        for id_, employee in enumerate(self.employees):
            employee.id = id_

    def init_shifts_id_offline(self) -> None:
        """
        temporary method to assign id's to shifts
        """
        for id_, shift in enumerate(self.shifts):
            shift.id = id_

    def init_workload(self) -> dict[int, dict[int, list]]:
        workload_dict = {}
        for employee in self.employees:
            workload_dict[employee.id] = {weeknum: [] for weeknum in employee.availability}
        return workload_dict

    def init_coliding_dict(self) -> dict[int, list[int]]:

        time_conflict_dict = {shift.id: [] for shift in self.shifts}

        for i, shift_1 in enumerate(self.shifts):

            for shift_2 in self.shifts[i+1:]:
                if shift_1.end < shift_2.start:
                    continue
                if shift_1.start < shift_2.end:
                    time_conflict_dict[shift_1.id].append(shift_2.id)
                    time_conflict_dict[shift_2.id].append(shift_1.id)

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

        availabilities = []
        for employee in self.employees:

            for weeknum in employee.availability:
                for workable_shift in employee.availability[weeknum]:

                    if self.__possible_shift(workable_shift, employee, shift):
                        availabilities.append(employee.id)

        return availabilities

    def get_colliding_shifts(self, shift_id: int) -> list[int]:
        return self.time_conflict_dict.get(shift_id)

    def set_shift_occupation(self, shift_id: int, occupied: bool) -> None:
        if occupied:
            self.actual_availabilities[shift_id][0] = 1
        else:
            self.actual_availabilities[shift_id][0] = 0

    """ METHODS """

    def schedule_in(self, employee_id: int, shift_id: int) -> None:
        self.schedule[shift_id] = employee_id
        self.__update_workload(employee_id, shift_id, add=True)

        week_num = self.get_weeknumber(shift_id)
        employee_obj = self.get_employee(employee_id)
        emlployee_week_max = employee_obj.get_week_max(week_num)

        if len(self.workload[employee_id][week_num]) == emlployee_week_max:
            self.update_availabilty(employee_id, shift_id, added=True, max_hit=True)
        else:
            self.update_availabilty(
                employee_id, shift_id, added=True, max_hit=False)

    def schedule_out(self, shift_id: int) -> None:
        employee_id = self.schedule[shift_id]
        self.schedule[shift_id] = None
        self.__update_workload(employee_id, shift_id, add=False)
    
        self.update_availabilty(employee_id, shift_id, added=False)

    def update_availabilty(self, employee_id: int, shift_id: int, added: bool, max_hit: bool = False) -> None:

        self.set_shift_occupation(shift_id, added)

        coliding_shifts = self.get_colliding_shifts(shift_id)

        if added:
            for coliding_shift_id in coliding_shifts:
                if employee_id in self.actual_availabilities[coliding_shift_id][1]:
                    self.actual_availabilities[coliding_shift_id][1].remove(
                        employee_id)

            if max_hit:
                for shift_id in self.actual_availabilities:
                    if employee_id in self.actual_availabilities[shift_id][1]:
                        self.actual_availabilities[shift_id][1].remove(employee_id)
        else:
            for shift_id in self.actual_availabilities:
                if employee_id in self.actual_availabilities[shift_id][1]:
                    self.actual_availabilities[shift_id][1].add(employee_id)
    
    def random_fill(self) -> None:

        filled = 0
        while filled < len(self.schedule):
            shift_id = random.choice(self.schedule)

            if self.schedule[shift_id] != None:
                continue

            selected_employee = random.choice(self.employees)
            self.schedule_in(selected_employee.id, shift_id)

            filled += 1

    def greedy_fill(self) -> None:

        filled = 0
        while filled < len(self.schedule):

            sorted_id_list = sorted(self.schedule.keys(), key = lambda shift_id: len(self.actual_availabilities[shift_id][1]) if self.actual_availabilities[shift_id][0] == 0 else 999)

            for shift_id in sorted_id_list:
                if self.schedule[shift_id] != None:
                    continue
                # if len(self.actual_availabilities[sorted_id_list[0]][1]) < 2:
                #     shift_id = sorted_id_list[0]
                elif len(self.actual_availabilities[shift_id][1]) < 1:
                    raise LookupError('No availabilities for shift!')

                weeknum = self.get_weeknumber(shift_id)

                self.compute_priority(weeknum)
                self.update_highest_priority_list()

                possible_employee_list = list(self.actual_availabilities[shift_id][1])
                selected_employee_id = random.choice(possible_employee_list)
                
                for employee_id in possible_employee_list:
                    if self.get_employee(employee_id).priority < self.get_employee(selected_employee_id).priority:
                        selected_employee_id = employee_id
                
                self.schedule_in(selected_employee_id, shift_id)

                if not self.passed_hard_constraints(shift_id):
                    self.schedule_out(shift_id)
                else:
                    filled += 1

    def compute_priority(self, weeknum: int) -> None:
        for employee in self.employees:
            workload = self.get_workload(employee.id)
            week_max = employee.get_week_max(weeknum)
            week_min = employee.get_week_min(weeknum)

            if weeknum in employee.availability:
                availability_priority = (
                    len(employee.availability[weeknum]) - week_max)
                week_min_priority = (len(workload[weeknum]) - week_min)
                week_max_priority = (week_max - len(workload[weeknum]))

                if availability_priority < 1:
                    availability_priority = -99
                if week_min_priority < 0:
                    week_min_priority = -150
                if week_max_priority < 1:
                    week_max_priority = -99

                employee.priority = availability_priority + \
                    week_min_priority - week_max_priority
                # print(employee.name, employee.priority, week_min, week_max, len(workload[weeknum]))
            else:
                employee.priority = 999

    def update_highest_priority_list(self) -> None:
        self.priority_list = sorted(
            self.employees, key=lambda employee: employee.priority)

    def improve(self) -> None:
        for i in range(2000):
            # print(i)
            self.mutate()
        # print(self.compute_wage_cost(self.schedule) + self.standard_cost(self.employees))
   

    def print_schedule(self) -> None:
        # Format and print the schedule
        for shift_id, employee_id in self.schedule.items():
            print(self.get_shift(shift_id), self.get_employee(employee_id))


    """ COST FUNCTION """



    def compute_wage_cost(self, schedule:dict[int, int]) -> float:
        total_cost = 0
        for shift_id, employee_id in schedule.items():
            total_cost += self.__compute_cost(shift_id, employee_id)
        return round(total_cost, 2)
    
    @staticmethod
    def compute_replacement_factor(availabilities_dict: dict[int, set[int]]) -> float:

        def find_min_and_max(availabilities_dict: dict[int, tuple[bool, set[int]]]) -> tuple[int, int]:
            max_len_shift = sorted(availabilities_dict, key = lambda shift_id: len(availabilities_dict[shift_id][1]), reverse=True)[0]
            min_len_shift = sorted(availabilities_dict, key = lambda shift_id: len(availabilities_dict[shift_id][1]))[0]

            max_len = len(availabilities_dict[max_len_shift][1])
            min_len = len(availabilities_dict[min_len_shift][1])

            return max_len, min_len
        
        max_len, min_len = find_min_and_max(availabilities_dict)
        
        return (max_len - min_len) / max (1, min_len)

    def compute_team_strength(self) -> float:
        ...

    @staticmethod
    def standard_cost(employee_list: list[Employee]):
        """
        calculates the total costs of a schedule
        """
        # calculate the starting costs
        total = sum([sum(employee.weekly_min.values()) * employee.get_wage()  for employee in employee_list])

        return round(total, 2)

    def mutate(self):  # this will probably be a class one day...
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''

        # pick a shift to replace
        shift_to_replace_id = self.__get_random_shift()
        current_employee_id = self.schedule[shift_to_replace_id]
        shift_obj = self.id_shift[shift_to_replace_id]

        # pick an employee that can work that shift
        possible_employee_id = self.__get_random_employee(
            shift_to_replace_id, current_employee_id)  # Updated to get only the Employee object

        # use duration to calculate cost
        new_cost = self.__compute_cost(
            shift_to_replace_id, possible_employee_id)  # Access the wage directly

        # check if costs are lower with this employee than previous
        current_employee_obj = self.get_employee(current_employee_id)
        current_cost = current_employee_obj.wage * shift_obj.duration

        if new_cost < current_cost:

            # check if employee is not crossing weekly_max and place shift into workload
            if self.__workload(possible_employee_id, shift_to_replace_id): # can this be shift_id?

                # add shift to workload dictionary
                if self.passed_hard_constraints(shift_to_replace_id):
                    self.schedule[shift_to_replace_id] = possible_employee_id

            else:
                # print('starting')
                # print(possible_employee_id, shift_to_replace_id)
                # print(self.schedule)
                # print(' ------------------------------------------------------- ')

                # get the total schedule costs before changes:
                total_costs_old = self.compute_wage_cost(self.schedule) + self.standard_cost(self.employees)

                # make changes
                undo_update = self.mutate_max_workload(possible_employee_id, shift_to_replace_id) # new worker has updated his workload, old worker had that shift removed from workload
                total_costs_new = self.compute_wage_cost(self.schedule) + self.standard_cost(self.employees)

                # compare costs
                if total_costs_new > total_costs_old:
                    for update in undo_update:
                        # update the temporarly placed worker's workload
                        employee_id, shift_id = update

                        # remove current worker from schedule and update workload
                        self.__update_workload( self.schedule[shift_id], shift_id, add=False)
                        self.schedule[shift_id] = employee_id
                        self.__update_workload(employee_id, shift_id, add=True)
                        
                #     print('did not improve')
                # print(self.schedule)
                # print('done')
    def mutate_max_workload(self, possible_employee_id, shift_to_replace_id):
        '''
        Method gets called when mutate wants to schedule a worker for a shift but the worker is already
        working his/hers max. This method will replace one of his/her shifts to check if that will be cheaper
        '''

        undo_update: tuple(int, int) = []

        # get the shortest shift the busy person is working
        shortest_shift_id = sorted(self.shifts, key=lambda x: x.duration)[0].id

        if shift_to_replace_id == shortest_shift_id:
            return

        # pick new employee to work the shortest shift
        shortest_shift_employee_id = self.__get_random_employee(shortest_shift_id, possible_employee_id)

        if self.__workload(shortest_shift_employee_id, shortest_shift_id):
            if self.passed_hard_constraints(shortest_shift_id):

                # store the changes ('old employee, shift')
                undo_update.append((self.schedule[shortest_shift_id], shortest_shift_id))
                self.__update_workload(shortest_shift_employee_id, shortest_shift_id, add=True)
                self.__update_workload(possible_employee_id, shift_to_replace_id, add=False)
                self.schedule[shortest_shift_id] = shortest_shift_employee_id
        else:
            self.mutate_max_workload(shortest_shift_employee_id, shortest_shift_id)

        return undo_update

    """ HARD CONSTRAINTS """

    def passed_hard_constraints(self, shift_id: int) -> bool:
        if not self.same_time(shift_id):
            return False
        return True

    def same_time(self, shift_id: int) -> bool:
        employee_id = self.schedule[shift_id]

        if employee_id is None:
            raise ValueError('No employee in the schedule')

        colliding_shifts = self.get_colliding_shifts(shift_id)
        for colliding_shift_id in colliding_shifts:
            if self.schedule[colliding_shift_id] == employee_id:
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

    def __get_random_shift(self) -> int:
        """
        returns a tuple with inside (1) a tuple containing shift info and (2) an index
        """
        return random.choice(self.shifts).get_id()

        random_shift = random.choice(self.shifts.keys())

        return random_shift

    def __get_random_employee(self, shift_to_replace_id, current_id) -> int:
        """
        returns an employee id
        """

        # make sure we do not select current employee
        choices = set(self.availabilities[shift_to_replace_id]) - set([current_id,])
        return random.choice(list(choices))

    def __compute_cost(self, shift: int, possible_employee_id: int) -> float:
        """
        returns the total pay using the wage and shift in hours. Also takes into account that if an employee has a
        weekly min, the first shifts are 'free'
        """

        possible_employee_object = self.get_employee(possible_employee_id)
        employee_shifts = self.get_workload(possible_employee_id)
        weeknumber = self.get_weeknumber(shift)
        weekly_min = possible_employee_object.get_week_min(weeknumber)
        hours = self.get_shift(shift).duration
        wage = possible_employee_object.get_wage()
        employee_workload = self.workload[possible_employee_id]

        # if week not in workload, number of shifts that week == 0
        if weeknumber not in employee_workload and weekly_min > 0:

            # this shift the worker works for 'free'
            return 0

        # check if worker is under his/hers weely min
        elif len(employee_workload[weeknumber]) < weekly_min:
            return 0

        else:
            # if weekly_min is reached, calculate the wage it will cost normal way
            return wage * hours  # Multiply duration with hourly wage to get total pay

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
