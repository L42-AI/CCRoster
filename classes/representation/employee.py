import random
from datetime import date, time
from classes.representation.availability import Availability

class Employee:
    def __init__(self, fname, lname, av, maximum, wage, level, task, location) -> None:
        self.fname = fname
        self.lname = lname
        self.name= fname + " " + lname
        self.id = None
        self.availability: list[Availability] = self.init_availability(av)
        self.wage = wage
        self.weekly_max = maximum
        self.level = level
        self.tasks = 1 if task=='everything' else 0
        self.location = location # where does this employee work? coffecompany, bagels and beans or google?
        self.add_remove_timeslot = []

        # self.upload_employee()
        # self.upload_availability()

    """ Init """

    def init_availability(self, av):
        """
        Initiates the availability list of an employee with data objects"""
        availability = []
        for entry in av:
            start_datetime = entry[0]
            end_datetime = entry[1]
            availability.append(Availability(start=start_datetime, end=end_datetime))
        return availability


    """ Upload """
    def upload_employee(self):


        # translate the string to a code corresponding with the location
        if self.location == 'coffee_company':
            location = 1
        if self.tasks == 'everything':
            task = 1

        # add the employee to the database
        query = "INSERT INTO Employee (lname, fname, hourly, level, task, location) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (self.lname, self.fname, self.wage, self.level, task, location)
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
        query = "INSERT INTO Availability (employee_id, week, day, shift, weekly_max) VALUES (%s, %s, %s, %s, %s)"
        for entry in self.availability:
            values = (self.id, entry[0], entry[1], entry[2], self.weekly_max[entry[0]])
            self.cursor.execute(query, values)
        self.db.commit()

    def change_availability(self):
        '''
        goes trough a list of changes and applies them to the database
        '''
        for change in self.add_remove_timeslot:
            if change[0] == 'add':
                query = "INSERT INTO Availability (employee_id, week, day, shift, weekly_max) VALUES (%s, %s, %s, %s, %s)"
                values = (self.id, change[1][0], change[1][1], change[1][2], self.weekly_max[change[1][0]])
                self.cursor.execute(query, values)
            else:
                query = "DELETE FROM Availability WHERE employee_id = %s AND week = %s AND day = %s AND shift = %s "
                values = (self.id, change[1][0], change[1][1], change[1][2])
                self.cursor.execute(query, values)

        # clear the list, we do not want to run old commands
        self.add_remove_timeslot = []

    '''
    update
    '''
    def update_availability(self, availability):
        self.availability = []
        for entry in availability:
            if entry[0] == self.id:
                self.availability.append(entry)


    """ Get """
    def get_name(self):
        return self.name

    def get_full_av(self) -> set:
        return self.availability

    def get_av(self) -> list[int]:
        if len(self.availability) > 0:
            return random.choice(self.availability)

    def get_name(self, name) -> str:
        return name

    def get_wage(self) -> float:
        return float(self.wage)

    def get_level(self) -> int:
        return self.level

    def get_tasks(self) -> int:
        return self.tasks

    def get_week_max_dict(self) -> dict:
        return self.weekly_max

    def get_week_max(self, week) -> int:
        return self.weekly_max.get(week)

    def get_id(self) -> int:
        return self.id

