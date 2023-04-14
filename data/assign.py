from datetime import datetime

from classes.representation.dataclasses import Shift, Availability
from classes.representation.employee import Employee


employee_list: list[Employee] = []
shift_list: list[Shift] = []

employee_list.append(Employee('Emma', 'Deckers', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                  Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                  Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                  Availability(start=datetime(2023,2,3,0), end=datetime(2023,2,3,23,59))],
                                                  {5:2, 1:2, 2:2, 3:2}, {5:1, 1:1, 2:1, 3:1}, 24, 1, [1], 'coffee_company'))

employee_list.append(Employee('Soraya', 'van Geldere', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                        Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                        Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59))],
                                                        {5:4, 1:4, 2:4, 3:4}, {5:1, 1:1, 2:1, 3:1}, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee("Sophie", "van 't Hullenaar", [Availability(start=datetime(2023,2,3,13,3), end=datetime(2023,2,3,23,59)),
                                                             Availability(start=datetime(2023,2,4,0), end=datetime(2023,2,4,23,59)),
                                                             Availability(start=datetime(2023,2,5,0), end=datetime(2023,2,5,23,59))],
                                                             {5:2, 1:2, 2:2, 3:2}, {5:1, 1:1, 2:1, 3:1}, 12, 1, [1], 'coffee_company'))

employee_list.append(Employee('Isabella', 'Koster', [Availability(start=datetime(2023,1,30,7,3), end=datetime(2023,1,30,18,00)),
                                                     Availability(start=datetime(2023,1,31,7,3), end=datetime(2023,1,31,18,00)),
                                                     Availability(start=datetime(2023,2,4,8,3), end=datetime(2023,2,4,13,30))],
                                                     {5:2, 1:2, 2:2, 3:2}, {5:1, 1:1, 2:1, 3:1}, 11, 1, [1], 'coffee_company'))

employee_list.append(Employee('Alexandra', 'Offringa', [Availability(start=datetime(2023,2,3,0), end=datetime(2023,2,3,23,59))],
                                                       {5:1, 1:0, 2:0, 3:0}, {5:1, 1:1, 2:1, 3:1}, 15.5, 1, [1], 'coffee_company'))

employee_list.append(Employee('Pim', 'Putman', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,14)),
                                                Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59))],
                                                {5:2, 1:0, 2:0, 3:0}, {5:1, 1:1, 2:1, 3:1}, 16.60, 1, [1], 'coffee_company'))

employee_list.append(Employee('Danaë', 'Verstegen', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                     Availability(start=datetime(2023,1,31,7,3), end=datetime(2023,1,31,13,00)),
                                                     Availability(start=datetime(2023,2,5,8,3), end=datetime(2023,2,5,13,30))],
                                                     {5:2, 1:2, 2:2, 3:2}, {5:1, 1:1, 2:1, 3:1}, 14, 1, [1], 'coffee_company'))

employee_list.append(Employee('Miranda', 'van Vuren', [Availability(start=datetime(2023,1,30,0), end=datetime(2023,1,30,23,59)),
                                                       Availability(start=datetime(2023,1,31,0), end=datetime(2023,1,31,23,59)),
                                                       Availability(start=datetime(2023,2,1,0), end=datetime(2023,2,1,23,59)),
                                                       Availability(start=datetime(2023,2,2,0), end=datetime(2023,2,2,23,59)),
                                                       Availability(start=datetime(2023,2,5,0), end=datetime(2023,2,5,23,59))],
                                                       {5:2, 1:2, 2:2, 3:2}, {5:1, 1:1, 2:1, 3:1}, 18, 1, [1], 'coffee_company'))

employee_list.append(Employee('Lulu', 'Wolff', [Availability(start=datetime(2023,2,4,0), end=datetime(2023,2,4,23,59))],
                                                {5:1, 1:0, 2:0, 3:0}, {5:1, 1:1, 2:1, 3:1}, 11, 1, [1], 'coffee_company'))

employee_list.append(Employee('Tamar', 'van der Zalm', [Availability(start=datetime(2023,2,1,13), end=datetime(2023,2,1,23,59)),
                                                        Availability(start=datetime(2023,2,2,7), end=datetime(2023,2,2,18,00))],
                                                        {5:2, 1:2, 2:2, 3:2}, {5:1, 1:1, 2:1, 3:1}, 30, 1, [1], 'coffee_company'))

for day in range(30,32):
    shift_list.append(Shift(start=datetime(2023, 1, day, 7, day),
                         end=datetime(2023, 1, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 1, day, 12, 30),
                         end=datetime(2023, 1, day, 18, 0),
                         task=1, location=1))

for day in range(1,6):
    shift_list.append(Shift(start=datetime(2023, 2, day, 7, day),
                         end=datetime(2023, 2, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 2, day, 12, 30),
                         end=datetime(2023, 2, day, 18, 0),
                         task=1, location=1))
