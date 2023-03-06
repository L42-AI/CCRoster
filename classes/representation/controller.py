import queue
import threading


from classes.representation.employee import Employee
from classes.representation.shift import Shift
from data.queries import db_cursor, downloading_availability
from classes.representation.generator import Generator


class Controller:
    def __init__(self, location) -> None:
        self.employee_list: list[Employee] = []
        self.shift_list: list[Shift] = []
        self.location = location
        self.db, self.cursor = db_cursor()
        self.queue = queue.Queue()
        self.name_to_id = {}
        self.close = False
        self.threading()


    """ Get """

    def get_employee_list(self) -> list:
        return self.employee_list

    def get_shift_list(self) -> list:
        return self.shift_list

    def get_start_and_finish_time(self, time: str) -> tuple:
        return time.split(' - ')

    def get_shift_info(self, info: dict) -> tuple:
        return info['day'], info['week'], info['type']

    """ Methods """
    def threading(self):
        t = threading.Thread(target=self.communicate_server)
        t.start()
        if self.close:
            print('close')
            self.cursor.close()
            self.db.close()
            return


    def create_employee(self, lname, fname, hourly_wage, level, tasks):
        employee = Employee(
            lname = lname,
            fname = fname,
            av = [],
            maximum={},
            wage = hourly_wage,
            level = level,
            task = tasks,
            location = self.location
            )

        # add employee locally
        self.employee_list.append(employee)
        self.name_to_id[fname+lname] = employee.id

        # add employee in database
        self.queue.put(("INSERT INTO Employee (lname, fname, hourly, level, task, location) VALUES (%s, %s, %s, %s, %s, %s)", (lname, fname, hourly_wage, level, tasks, self.location)))

    def edit_employee_availability(self, employee: Employee, availability_slot: list[int], add: bool):
        # for employee_instance in self.employee_list:
        #     if employee_instance == employee:
        #         print(len(employee_instance.availability))

        # collect info for queries
        id = employee.id
        week = availability_slot[0]
        day = availability_slot[1]
        shift =availability_slot[2]

        if add:
            employee.availability.append(availability_slot)
            self.queue.put(("INSERT INTO Availability (employee_id, week, day, shift, weekly_max_employee) VALUES (%s, %s, %s, %s, %s)"), (id, week, day, shift, employee.weekly_max_employee[week]))
        else:
            employee.availability.remove(availability_slot)
            self.queue.put(("DELETE FROM Availability WHERE employee_id = %s AND week = %s AND day = %s AND shift = %s "), (id, week, day, shift))

        for employee_instance in self.employee_list:
            if employee_instance == employee:
                print(len(employee_instance.availability))

    def delete_employee(self, fname, lname):
        id = self.name_to_id[fname+lname]
        for employee_instance in self.employee_list:
            if employee_instance.name == employee_instance.get_full_name(fname, lname):
                self.employee_list.remove(employee_instance)
                self.queue.put(("DELETE FROM Employee WHERE id=%s", (id,)))
                break

    def create_shift(self, time: str, day: int, week: int, task: int) -> None:
        start_time, end_time = self.get_start_and_finish_time(time)

        self.shift_list.append(
            Shift(
            start_time = start_time,
            end_time = end_time,
            day = day,
            week = week,
            task = task,
            location = self.location
            )
        )

        self.queue.put(("INSERT INTO Shifts (location, week, day, start, end, task) VALUES (%s, %s, %s, %s, %s, %s)", (self.location, week, day, start_time, end_time, task)))


    def delete_shift(self, time: str) -> None:
        self.to_delete: list[Shift] = []
        start_time, end_time = self.get_start_and_finish_time(time)

        for shift_instance in self.shift_list:
            if shift_instance.start_time == start_time and shift_instance.end_time == end_time:
                self.to_delete.append(shift_instance)
                self.queue.put(("DELETE FROM Shifts WHERE start = %s AND end = %s", (start_time, end_time)))

        for i in range(len(self.to_delete)):
            self.shift_list.remove(self.to_delete[i])

        self.communicate_server()

    def communicate_server(self):
        """ Function that gets called all the time to send the new data to the server and download data"""
        cursor = self.cursor
        connection = self.db
        print(1)
        while True:
            print(self.close)
            if not queue.Empty():
                query, data = self.queue.get()
                print('1')
                cursor.execute(query, data)
                print('2')
            av = downloading_availability(connection, cursor)
            print('3')
            connection.commit()
            print('4')
            if av != Generator.availability:
                print('different!')
            if self.employee_list != 


