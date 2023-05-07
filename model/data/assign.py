from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from model.representation.data_objects import Employee, Availability, Shift, Weekly_max, Task
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
database_url = 'mysql+mysqlconnector://Jacob:wouterisdebestehuisgenoot@185.224.91.162:3308/rooster'

engine = create_engine(database_url)
Base.metadata.create_all(engine)

session = Session(engine)


def create_employee_availability(employee: Employee):
    for av in employee.availability:
        session.add(av)


def create_employee_weekly_max(employee):
    for week, max_shifts in employee.weekly_max.items():
        wm = Weekly_max(week=week, max=max_shifts)
        wm.employee = employee
        session.add(wm)

def create_employee_tasks(employee):
    for task in employee.tasks:
        tsk = Task(employee_id=employee.id, task=task)
        session.add(tsk)


employee_list: list[Employee] = []
shift_list: list[Shift] = []

employee_list.append(Employee('Emma', 'Deckers', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                  Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                  Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                  Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                  Availability(start=datetime(2023,2,1,13), end=datetime(2023,2,1,23,59)),
                                                  Availability(start=datetime(2023,2,3,0), end=datetime(2023,2,3,23,59))],
                                                  {5:2, 1:2, 2:2, 3:2}, 4, 240, 1, [1], 'coffee_company'))
employee_list.append(Employee('Soraya', 'van Geldere', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                        Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                        Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)), ],
                                                        {5:2, 1:2, 2:2, 3:2}, 4, 3, 1, [1], 'coffee_company'))

employee_list.append(Employee("Sophie", "van 't Hullenaar", [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                        Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                        Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                        Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                        Availability(start=datetime(2023,2,3,13,3), end=datetime(2023,2,3,23,59)),
                                                        Availability(start=datetime(2023,2,4,0), end=datetime(2023,2,4,23,59)),
                                                        Availability(start=datetime(2023,2,5,0), end=datetime(2023,2,5,23,59))],
                                                             {5:2, 1:2, 2:2, 3:2}, 4, 12, 1, [1], 'coffee_company'))

employee_list.append(Employee('Isabella', 'Koster', [Availability(start=datetime(2023,2,3,13,3), end=datetime(2023,2,3,23,59)),
                                                             Availability(start=datetime(2023,2,4,0), end=datetime(2023,2,4,23,59)),
                                                             Availability(start=datetime(2023,2,5,0), end=datetime(2023,2,5,23,59)),
                                                    Availability(start=datetime(2023,1,30,7,3), end=datetime(2023,1,30,18,00)),
                                                     Availability(start=datetime(2023,1,31,7,3), end=datetime(2023,1,31,18,00)),
                                                     Availability(start=datetime(2023,2,4,8,3), end=datetime(2023,2,4,13,30))],
                                                     {5:2, 1:2, 2:2, 3:2}, 4, 11, 1, [1], 'coffee_company'))

employee_list.append(Employee('Alexandra', 'Offringa', [Availability(start=datetime(2023,2,3,0), end=datetime(2023,2,3,23,59))],
                                                       {5:1, 1:0, 2:0, 3:0}, 4, 200.5, 1, [1], 'coffee_company'))

employee_list.append(Employee('Pim', 'Putman', [Availability(start=datetime(2023,2,3,0), end=datetime(2023,2,3,23,59)),
                                                Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,14)),
                                                Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59))],
                                                {5:2, 1:0, 2:0, 3:0}, 4, 16.60, 1, [1], 'coffee_company'))

employee_list.append(Employee('Danaë', 'Verstegen', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                    Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                    Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                    Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,14)),
                                                     Availability(start=datetime(2023,1,31,7,3), end=datetime(2023,1,31,13,00)),
                                                     Availability(start=datetime(2023,2,5,8,3), end=datetime(2023,2,5,13,30))],
                                                     {5:2, 1:2, 2:2, 3:2}, 4, 14, 1, [1], 'coffee_company'))

employee_list.append(Employee('Miranda', 'van Vuren', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                    Availability(start=datetime(2023,1,31,7,3), end=datetime(2023,1,31,13,00)),
                                                     Availability(start=datetime(2023,2,5,8,3), end=datetime(2023,2,5,13,30)),
                                                       Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                       Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                       Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                       Availability(start=datetime(2023,2,5,0), end=datetime(2023,2,5,23,59))],
                                                       {5:2, 1:2, 2:2, 3:2}, 4, 18, 1, [1], 'coffee_company'))

employee_list.append(Employee('Lulu', 'Wolff', [Availability(start=datetime(2023,2,4,0), end=datetime(2023,2,4,23,59))],
                                                {5:1, 1:0, 2:0, 3:0}, 4, 1, 1, [1], 'coffee_company'))

employee_list.append(Employee('Tamar', 'van der Zalm', [Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                        Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                       Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                       Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                       Availability(start=datetime(2023,2,1,13), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,7), end=datetime(2023,2,2,18,00))],
                                                        {5:2, 1:2, 2:2, 3:2}, 4, 50, 1, [1], 'coffee_company'))
employee_list.append(Employee('Dumdum', 'Dummy', [Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                        Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                       Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                       Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                       Availability(start=datetime(2023,2,1,13), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,7), end=datetime(2023,2,2,18,00))],
                                                        {5:2, 1:2, 2:2, 3:2}, 0, 100000, 1, [1], 'coffee_company'))


# short shifts
for day in range(30,32):
    shift_list.append(Shift(start=datetime(2023, 1, day, 10, 30),
                         end=datetime(2023, 1, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 1, day, 13, 30),
                         end=datetime(2023, 1, day, 18, 0),
                         task=1, location=1))
    
# medium shifts
for day in range(1,3):
    shift_list.append(Shift(start=datetime(2023, 2, day, 9, 0),
                         end=datetime(2023, 2, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 2, day, 14, 0),
                         end=datetime(2023, 2, day, 18, 0),
                         task=1, location=1))
    
# long shifts
for day in range(4,6):
    shift_list.append(Shift(start=datetime(2023, 2, day, 7, 30),
                         end=datetime(2023, 2, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 2, day, 12, 30),
                         end=datetime(2023, 2, day, 18, 0),
                         task=1, location=1))


# for emp in employee_list:
#     session.add(emp)
#     create_employee_tasks(emp)
#     create_employee_availability(emp)
#     create_employee_weekly_max(emp)

# if __name__ == 'main':
#     for shift in shift_list:
#         session.add(shift)
#     session.commit()
#     session.close()
