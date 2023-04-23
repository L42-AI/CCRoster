from datetime import datetime

from classes.representation.shift import Shift
from classes.representation.employee import Employee
from classes.representation.availability import Availability

employee_list: list[Employee] = []
shift_list: list[Shift] = []

employee_list.append(Employee('Emma', 'Deckers', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                  Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                  Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                  Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                  Availability(start=datetime(2023,2,1,13), end=datetime(2023,2,1,23,59)),
                                                  Availability(start=datetime(2023,2,3,0), end=datetime(2023,2,3,23,59))],
                                                  {5:2, 1:2, 2:2, 3:2}, {5:3, 1:3, 2:3, 3:3}, 240, 1, [1], 'coffee_company'))

employee_list.append(Employee('Soraya', 'van Geldere', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                        Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                        Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)), ],
                                                        {5:4, 1:4, 2:4, 3:4}, {5:3, 1:3, 2:3, 3:3}, 3, 1, [1], 'coffee_company'))

employee_list.append(Employee("Sophie", "van 't Hullenaar", [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                        Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                        Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                        Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                        Availability(start=datetime(2023,2,3,13,3), end=datetime(2023,2,3,23,59)),
                                                        Availability(start=datetime(2023,2,4,0), end=datetime(2023,2,4,23,59)),
                                                        Availability(start=datetime(2023,2,5,0), end=datetime(2023,2,5,23,59))],
                                                             {5:2, 1:2, 2:2, 3:2}, {5:3, 1:3, 2:3, 3:3}, 12, 1, [1], 'coffee_company'))

employee_list.append(Employee('Isabella', 'Koster', [Availability(start=datetime(2023,2,3,13,3), end=datetime(2023,2,3,23,59)),
                                                             Availability(start=datetime(2023,2,4,0), end=datetime(2023,2,4,23,59)),
                                                             Availability(start=datetime(2023,2,5,0), end=datetime(2023,2,5,23,59)),
                                                    Availability(start=datetime(2023,1,30,7,3), end=datetime(2023,1,30,18,00)),
                                                     Availability(start=datetime(2023,1,31,7,3), end=datetime(2023,1,31,18,00)),
                                                     Availability(start=datetime(2023,2,4,8,3), end=datetime(2023,2,4,13,30))],
                                                     {5:2, 1:2, 2:2, 3:2}, {5:3, 1:3, 2:3, 3:3}, 11, 1, [1], 'coffee_company'))

employee_list.append(Employee('Alexandra', 'Offringa', [Availability(start=datetime(2023,2,3,0), end=datetime(2023,2,3,23,59))],
                                                       {5:1, 1:0, 2:0, 3:0}, {5:3, 1:3, 2:3, 3:3}, 200.5, 1, [1], 'coffee_company'))

employee_list.append(Employee('Pim', 'Putman', [Availability(start=datetime(2023,2,3,0), end=datetime(2023,2,3,23,59)),
                                                Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,14)),
                                                Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59))],
                                                {5:2, 1:0, 2:0, 3:0}, {5:3, 1:3, 2:3, 3:3}, 16.60, 1, [1], 'coffee_company'))

employee_list.append(Employee('Danaë', 'Verstegen', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                    Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                    Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                    Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,14)),
                                                     Availability(start=datetime(2023,1,31,7,3), end=datetime(2023,1,31,13,00)),
                                                     Availability(start=datetime(2023,2,5,8,3), end=datetime(2023,2,5,13,30))],
                                                     {5:2, 1:2, 2:2, 3:2}, {5:3, 1:3, 2:3, 3:3}, 14, 1, [1], 'coffee_company'))

employee_list.append(Employee('Miranda', 'van Vuren', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                    Availability(start=datetime(2023,1,31,7,3), end=datetime(2023,1,31,13,00)),
                                                     Availability(start=datetime(2023,2,5,8,3), end=datetime(2023,2,5,13,30)),
                                                       Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                       Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                       Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                       Availability(start=datetime(2023,2,5,0), end=datetime(2023,2,5,23,59))],
                                                       {5:2, 1:2, 2:2, 3:2}, {5:3, 1:3, 2:3, 3:3}, 18, 1, [1], 'coffee_company'))

employee_list.append(Employee('Lulu', 'Wolff', [Availability(start=datetime(2023,2,4,0), end=datetime(2023,2,4,23,59))],
                                                {5:1, 1:0, 2:0, 3:0}, {5:3, 1:3, 2:3, 3:3}, 1, 1, [1], 'coffee_company'))

employee_list.append(Employee('Tamar', 'van der Zalm', [Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                        Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                       Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                       Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                       Availability(start=datetime(2023,2,1,13), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,7), end=datetime(2023,2,2,18,00))],
                                                        {5:2, 1:2, 2:2, 3:2}, {5:3, 1:3, 2:3, 3:3}, 50, 1, [1], 'coffee_company'))
employee_list.append(Employee('Dumdum', 'Dummy', [Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                        Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                       Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                       Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                       Availability(start=datetime(2023,2,1,13), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,7), end=datetime(2023,2,2,18,00))],
                                                        {5:2, 1:2, 2:2, 3:2}, {5:0, 1:0, 2:0, 3:0}, 1000, 1, [1], 'coffee_company'))

# for day in range(30,32):
#     shift_list.append(Shift(start=datetime(2023, 1, day, 7, day),
#                          end=datetime(2023, 1, day, 13, 0),
#                          task=1, location=1))
#     shift_list.append(Shift(start=datetime(2023, 1, day, 12, 30),
#                          end=datetime(2023, 1, day, 18, 0),
#                          task=1, location=1))

# for day in range(1,6):
#     shift_list.append(Shift(start=datetime(2023, 2, day, 7, day),
#                          end=datetime(2023, 2, day, 13, 0),
#                          task=1, location=1))
#     shift_list.append(Shift(start=datetime(2023, 2, day, 12, 30),
#                          end=datetime(2023, 2, day, 18, 0),
#                          task=1, location=1))

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

for id_, employee in enumerate(employee_list):
    employee.id = id_

for id_, shift in enumerate(shift_list):
    shift.id = id_

def possible_shift(workable_shift: Availability, employee: Employee, shift: Shift) -> bool:

    # Check time
    if workable_shift.start > shift.start or workable_shift.end < shift.end:
        return False

    # Check task
    tasks_list = employee.get_tasks()
    for task in tasks_list:
        if task == shift.task:
            return True
    return False

def get_employee_set(shift: Shift) -> set[int]:
    """
    this method is only used to develop the generator, later, the info will actually be downloaded
    for now it just returns a hardcoded list with availability
    """

    availabilities = set()
    for employee in employee_list:

        for weeknum in employee.availability:
            for workable_shift in employee.availability[weeknum]:

                if possible_shift(workable_shift, employee, shift):
                    availabilities.add(employee.id)

    return availabilities

def init_coliding_dict(shifts: list[Shift]) -> dict[int, list[int]]:

    time_conflict_dict = {shift.id: [] for shift in shifts}

    for i, shift_1 in enumerate(shifts):

        for shift_2 in shifts[i+1:]:
            if shift_1.end < shift_2.start:
                continue
            if shift_1.start < shift_2.end:
                time_conflict_dict[shift_1.id].append(shift_2.id)
                time_conflict_dict[shift_2.id].append(shift_1.id)

    return time_conflict_dict

time_conflict_dict = init_coliding_dict(shift_list)
total_availabilities = {shift.id: get_employee_set(shift) for shift in shift_list}

