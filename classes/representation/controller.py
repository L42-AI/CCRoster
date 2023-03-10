import queue
import threading
import time
from enum import Enum
from datetime import date, timedelta

from classes.representation.employee import Employee
from classes.representation.dataclasses import Shift, Availability

from data.assign import employee_list, shift_list
from data.queries import db_cursor, downloading_availability, downloading_shifts, downloading_employees

LOCK = threading.Lock()
SLEEP = 10 # timer in seconds to slow down the background loading of the program

class Controller:
    def __init__(self, location) -> None:
        # self.generator = generator
        self.location = location

        # Set tasks and levels
        """ TEMPORARY UNTIL CONNECTED TO SETTINGS PAGE """
        self.update_levels()
        self.update_tasks()

        # Create enums
        """ TEMPORARY UNTIL CONNECTED TO SETTINGS PAGE """
        self.update_levels_enum()
        self.update_tasks_enum()

        self.employee_list: list[Employee] = employee_list
        self.shift_list: list[Shift] = shift_list
        self.update_employee_dict(self.employee_list)
        self.update_shift_dict(self.shift_list)
        self.name_to_id = {}

        self.db, self.cursor = db_cursor()
        self.availability = downloading_availability(self.db, self.cursor, location)
        self.shifts = downloading_shifts(self.db, self.cursor, self.location)
        self.queue = queue.Queue()
        self.close = False
        self.threading()
        self.tasktypes = {1: 'Allround', 2:'Bagels', 3:'Koffie', 4:'Kassa'}
        self.days = {0:'Maandag', 1:'Dinsdag', 2:'Woensdag', 3:'Donderdag', 4:'Vrijdag', 5:'Zaterdag', 6:'Zondag'}

        self.start_date = self.get_monday(self.get_last_day_of_month())
        self.end_date = self.get_monday(self.get_last_day_of_month(months_into_future=1))

    """ GET """

    def get_last_day_of_month(self, months_into_future: int = 0) -> date:
        today = date.today()
        last_day_of_month = today.replace(month=today.month + months_into_future + 1, day=1) - timedelta(1)
        return last_day_of_month

    def get_monday(self, last_day_of_month: date) -> date:
        first_monday_of_next_month = last_day_of_month + timedelta(days=(7-last_day_of_month.weekday()))
        return first_monday_of_next_month

    def get_start_and_finish_time(self, time: str) -> tuple:
        return time.split(' - ')

    def get_shift_info(self, info: dict) -> tuple:
        return info['day'], info['week'], info['type']

    def get_start_date(self) -> date:
        return self.start_date

    def get_end_date(self) -> date:
        return self.end_date

    def get_employee_list(self) -> list:
        return self.employee_list

    def get_shift_list(self) -> list:
        return self.shift_list

    def get_Levels_enum(self) -> Enum:
        return self.Levels

    def get_Tasks_enum(self) -> Enum:
        return self.Tasks

    def get_shift_list_from(self, task: str) -> list[Shift]:
        task_num: int = self.Tasks[task].value
        return self.shift_dict[task_num]

    def get_employee_list_from(self, task: str) -> list[Employee]:
        task_num: int = self.Tasks[task].value
        return self.employee_dict[task_num]

    """ Input methods for the GUI"""

    def shifts_input(self):
        shifts = downloading_shifts(self.db, self.cursor, self.location)
        for _, shift in enumerate(shifts):
            week, day, start, end, task = shift
            shifts[_] = (f'{self.tasktypes[task]} shift in week {week} op {self.days[day]} vanaf {start} tot {end}', task)
        return shifts

    def employees_input(self):
        '''
        method that provides the employee info a user sees when opening the GUI
        '''
        employees = downloading_employees(self.db, self.cursor, self.location)
        for _, employee in enumerate(employees):
            fname, lname, hourly, level, task = employee
            employees[_] = f'NAAM:{fname} {lname} SALARIS: {hourly} LEVEL: {level} TAAK: {task}'
        return employees

    """" Update """

    def update_employee_dict(self, employee_list: list[Employee]) -> dict[int: list[Shift]]:
        self.employee_dict = {task.value: [] for task in self.Tasks}

        for employee in employee_list:
            for task in employee.tasks:
                task_num = self.Tasks[task].value
                self.employee_dict[task_num].append(employee)

    def update_shift_dict(self, shift_list: list[Shift]) -> dict[int: list[Shift]]:
        self.shift_dict = {task.value: [] for task in self.Tasks}

        [self.shift_dict[shift.task].append(shift) for shift in shift_list]

    """ Methods """

    def generate(self):
        self.generator.improve()

    def create_employee(self, lname: str, fname: str, hourly_wage: int, level: int, tasks: int):
        for task in tasks:
            employee = Employee(
                lname = lname,
                fname = fname,
                av = [],
                maximum = {},
                wage = hourly_wage,
                level = level,
                task = task,
                location = self.location
                )

            # add employee locally
            self.employee_list.append(employee)
            self.name_to_id[fname+lname] = employee.id

            # add employee in database
            self.queue.put(("INSERT INTO Employee (fname, lname, hourly, level, task, location) VALUES (%s, %s, %s, %s, %s, %s)", (lname, fname, hourly_wage, level, task, self.location)))

    def edit_employee_availability(self, employee: Employee, availability: Availability, add: bool):
        '''
        method that changes the availability from an employee both locally and online
        '''

        # collect info for queries
        id = employee.id
        availability_start = availability.start
        availability_end = availability.end

        # add or remove employee both locally and in the database
        """ FIX NEEDED FOR SERVER INTERACTION """
        """ AVAILABILITY NOT SLOT ANYMORE BUT OBJECT """
        if add:
            employee.availability.append(availability)
            # self.queue.put(("INSERT INTO Availability (employee_id, week, day, shift, weekly_max) VALUES (%s, %s, %s, %s, %s)"), (id, week, day, shift, employee.weekly_max[week]))
        else:
            employee.availability.remove(availability)
            # self.queue.put(("DELETE FROM Availability WHERE employee_id = %s AND week = %s AND day = %s AND shift = %s "), (id, week, day, shift))

    def delete_employee(self, fname, lname):
        '''
        method to delete an employee both locally and from the server
        '''
        id = self.name_to_id[fname+lname]
        for employee_instance in self.employee_list:
            if employee_instance.id == id:
                self.employee_list.remove(employee_instance)

                # delete employee from the database
                self.queue.put(("DELETE FROM Employee WHERE id=%s", (id,)))
                break

    def update_employee_availability_local(self, new_av: list[tuple]):
        ''''
        updates the availability of the LOCAL employee instance that the GUI uses
        '''
        for employee in self.employee_list:
            mask = [x[0] == employee.id for x in new_av]
            employee.availability = [x for x, i in enumerate(new_av) if mask[i]]


    def create_shift(self, time: str, day: int, week: int, task: int) -> None:
        '''
        method to create locally and online a shift instance
        '''
        start_time, end_time = self.get_start_and_finish_time(time)

        self.shift_list.append(
            Shift(
            start = start_time,
            end = end_time,
            day = day,
            week = week,
            task = task,
            location = self.location
            )
        )

        # upload the shift to the database
        self.queue.put(("INSERT INTO Shifts (location, week, day, start, end, task) VALUES (%s, %s, %s, %s, %s, %s)", (self.location, week, day, start_time, end_time, task)))

    def delete_shift(self, time: str) -> None:
        self.to_delete: list[Shift] = []
        start_time, end_time = self.get_start_and_finish_time(time)

        for shift_instance in self.shift_list:
            if shift_instance.start_time == start_time and shift_instance.end_time == end_time:
                self.to_delete.append(shift_instance)

                # delete shift from database
                self.queue.put(("DELETE FROM Shifts WHERE start = %s AND end = %s AND location = %s", (start_time, end_time, self.location)))

        for i in range(len(self.to_delete)):
            self.shift_list.remove(self.to_delete[i])


    def threading(self):
        '''
        starts a new thread where communicate_server can run on so it does not slow down the application
        '''

        # deamon condition to indicate it should close when main thread closes too
        tread = threading.Thread(target=self.communicate_server, daemon=True)
        tread.start()
        if self.close:
            self.cursor.close()
            self.db.close()
            return

    def store_availability(self, new_availability, lock):
        '''
        stores new availability LOCAL in controller class. Uses lock to prevent GUI
        and controller writing to availability at the same time
        '''
        lock.acquire()
        self.availability = new_availability
        lock.release()

    def communicate_server(self):
        """ Function that runs all the time to send the new data to the server and download data"""
        cursor = self.cursor
        connection = self.db

        # stop when GUI.py stops, turning self.close to True
        while not self.close:

            # program freezes is queue is empty so check before entering queue
            if not self.queue.empty():
                query, data = self.queue.get()
                print(data)
                cursor.execute(query, data)

            # perform check to see if employees changed their availability remotely
            av = downloading_availability(connection, cursor, self.location)

            connection.commit()

            # update controller availability
            if av != self.availability:
                self.store_availability(av, LOCK)
                self.update_employee_availability_local(av)

            # do not run at full speed
            time.sleep(SLEEP)

    """ Enum """

    def update_levels(self) -> None:
        """ TO BE CONNECTED TO SETTINGS PAGE """
        self.levels_dict = {'Stagair': 1, 'Manager': 2, 'Lead': 3}

    def update_tasks(self) -> None:
        """ TO BE CONNECTED TO SETTINGS PAGE """
        self.tasks_dict = {'Allround': 1, 'Begels': 2, 'Koffie': 3, 'Kassa': 4}

    def update_levels_enum(self) -> None:
        self.Levels = Enum("Level", {key: value for key, value in self.levels_dict.items()})

    def update_tasks_enum(self) -> None:
        self.Tasks = Enum("Task", {key: value for key, value in self.tasks_dict.items()})

