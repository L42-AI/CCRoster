from classes.representation.employee import Employee
from classes.representation.shift import Shift
from data.queries import db_cursor

class Controller:
    def __init__(self, location) -> None:
        self.employee_list: list[Employee] = []
        self.shift_list: list[Shift] = []
        self.location = location
        self.db, self.cursor = db_cursor()
        self.threads = []

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

    def create_employee(self, first_name, last_name, hourly_wage, level, tasks):
        employee = Employee(
            first_name = first_name,
            last_name = last_name,
            av = [],
            maximum={},
            wage = hourly_wage,
            level = level,
            task = tasks
            )
        self.employee_list.append(employee)
        self.threads.append(("INSERT INTO Employee (name, hourly, level, task, location) VALUES (%s, %s, %s, %s, %s)", ))

    def edit_employee_availability(self, employee: Employee, availability_slot: list[int], add: bool):
        for employee_instance in self.employee_list:
            if employee_instance == employee:
                print(len(employee_instance.availability))

        if add:
            employee.availability.append(availability_slot)
        else:
            employee.availability.remove(availability_slot)

        for employee_instance in self.employee_list:
            if employee_instance == employee:
                print(len(employee_instance.availability))

        self.communicate_server()

    def delete_employee(self, first_name, last_name):
        for employee_instance in self.employee_list:
            if employee_instance.name == employee_instance.get_full_name(first_name, last_name):
                self.employee_list.remove(employee_instance)
                break

        self.communicate_server()

    def create_shift(self, time: str, day: str, week: str, task: str) -> None:
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

        self.communicate_server()


    def delete_shift(self, time: str) -> None:
        self.to_delete: list[Shift] = []
        start_time, end_time = self.get_start_and_finish_time(time)

        for shift_instance in self.shift_list:
            if shift_instance.start_time == start_time and shift_instance.end_time == end_time:
                self.to_delete.append(shift_instance)

        for i in range(len(self.to_delete)):
            self.shift_list.remove(self.to_delete[i])
        
        self.communicate_server()

    def communicate_server(self, method, input):
        """ Function that gets called all the time to send the new data to the server """


from classes.representation.employee import Employee
from classes.representation.shift import Shift
