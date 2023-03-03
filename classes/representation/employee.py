import random
import mysql.connector

class Employee:
    def __init__(self, name, av, maximum, wage, level, task, location) -> None:
        self.name = name
        self.id = None
        self.availability = av
        self.wage = wage
        self.weekly_max_employee = maximum
        self.level = level
        self.task = task
        self.location = location # where does this employee work? coffecompany, bagels and beans or google?
        self.add_remove_timeslot = []

        self.db = mysql.connector.connect(
            host="185.224.91.162",
            port=3308,
            user="Jacob",
            password="wouterisdebestehuisgenoot",
            database="rooster" # niet veranderen
        )
        self.cursor = self.db.cursor()

        # self.upload_employee()
        # self.upload_availability()

    """ Upload """
    def upload_employee(self):


        # translate the string to a code corresponding with the location
        if self.location == 'coffee_company':
            location = 1
        if self.task == 'everything':
            task = 1

        # add the employee to the database
        query = "INSERT INTO Employee (name, hourly, level, task, location) VALUES (%s, %s, %s, %s, %s)"
        values = (self.name, self.wage, self.level, task, location)
        self.cursor.execute(query, values)
        self.id = self.cursor.lastrowid
        print(self.id)
        self.db.commit()

    def upload_availability(self):
        '''
        removes current availability and replaces it with new one. if there is nothing, it just uploads the availibility. 
        But when making changes, first everything must be deleted.
        '''
        # uploads the availability given in assign
        query = "INSERT INTO Availability (employee_id, week, day, shift, weekly_max_employee) VALUES (%s, %s, %s, %s, %s)"
        for entry in self.availability:
            values = (self.id, entry[0], entry[1], entry[2], self.weekly_max_employee[entry[0]])
            self.cursor.execute(query, values)
        self.db.commit()

    def change_availability(self):
        '''
        goes trough a list of changes and applies them to the database
        '''
        for change in self.add_remove_timeslot:
            if change[0] == 'add':
                query = "INSERT INTO Availability (employee_id, week, day, shift, weekly_max_employee) VALUES (%s, %s, %s, %s, %s)"
                values = (self.id, change[1][0], change[1][1], change[1][2], self.weekly_max_employee[change[1][0]])
                self.cursor.execute(query, values)
            else:
                query = "DELETE FROM Availability WHERE employee_id = %s AND week = %s AND day = %s AND shift = %s "
                values = (self.id, change[1][0], change[1][1], change[1][2])
                self.cursor.execute(query, values)

        # clear the list, we do not want to run old commands
        self.add_remove_timeslot = []


    """ Get """

    def get_full_av(self) -> set:
        return self.availability

    def get_av(self) -> list[int]:
        if len(self.availability) > 0:
            return random.choice(self.availability)

    def get_full_name(self, first_name, last_name) -> str:
        return f'{first_name}{last_name}'

    def get_abreviated_name(self) -> str:
        return f'{self.first_name[0]}. {self.last_name}'

    def get_wage(self) -> float:
        return float(self.wage)

    def get_onboarding(self) -> int:
        return self.onboarding

    def get_week_max_dict(self) -> dict:
        return self.weekly_max_employee

    def get_week_max(self, week) -> int:
        return self.weekly_max_employee.get(week)