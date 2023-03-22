from datetime import datetime

from classes.representation.dataclasses import Shift, Availability
from classes.representation.employee import Employee


employee_list: list[Employee] = []
shift_list: list[Shift] = []

"""
employee_list.append(Employee('Emma', 'Deckers', [Availability(datetime(2023, 4, 3, 7, 0), datetime(2023, 4, 3, 9, 0)),
                                                Availability(datetime(2023, 4, 10, 7, 0), datetime(2023, 4, 10, 9, 0)),
                                                Availability(datetime(2023, 4, 15, 7, 0), datetime(2023, 4, 15, 9, 0)),
                                                Availability(datetime(2023, 4, 30, 7, 0), datetime(2023, 4, 30, 9, 0)),
                                                Availability(datetime(2023, 4, 22, 7, 0), datetime(2023, 4, 22, 9, 0)),
                                                Availability(datetime(2023, 4, 13, 7, 0), datetime(2023, 4, 13, 9, 0)),
                                                Availability(datetime(2023, 4, 17, 7, 0), datetime(2023, 4, 17, 9, 0)),
                                                Availability(datetime(2023, 4, 12, 7, 0), datetime(2023, 4, 12, 9, 0))],
                                             {14:2, 15:2, 16:2, 17:2}, 24, 1, 1, 'coffee_company'))

employee_list.append(Employee('Soraya', 'van Geldere', [Availability(datetime(2023, 4, 13, 7, 0), datetime(2023, 4, 13, 9, 0)),
                                                Availability(datetime(2023, 4, 12, 7, 0), datetime(2023, 4, 12, 9, 0)),
                                                Availability(datetime(2023, 4, 16, 7, 0), datetime(2023, 4, 16, 9, 0)),
                                                Availability(datetime(2023, 4, 29, 7, 0), datetime(2023, 4, 29, 9, 0)),
                                                Availability(datetime(2023, 4, 23, 7, 0), datetime(2023, 4, 23, 9, 0)),
                                                Availability(datetime(2023, 4, 3, 7, 0), datetime(2023, 4, 3, 9, 0)),
                                                Availability(datetime(2023, 4, 17, 7, 0), datetime(2023, 4, 17, 9, 0)),
                                                Availability(datetime(2023, 4, 8, 7, 0), datetime(2023, 4, 8, 9, 0))],
                                                 {14:4, 15:4, 16:4, 17:4}, 10, 1, 1, 'coffee_company'))

employee_list.append(Employee("Sophie", "van 't Hullenaar", [Availability(datetime(2023, 4, 3, 7, 0), datetime(2023, 4, 3, 9, 0)),
                                                Availability(datetime(2023, 4, 8, 7, 0), datetime(2023, 4, 8, 9, 0)),
                                                Availability(datetime(2023, 4, 23, 7, 0), datetime(2023, 4, 23, 9, 0)),
                                                Availability(datetime(2023, 4, 14, 7, 0), datetime(2023, 4, 14, 9, 0)),
                                                Availability(datetime(2023, 4, 12, 7, 0), datetime(2023, 4, 12, 9, 0)),
                                                Availability(datetime(2023, 4, 26, 7, 0), datetime(2023, 4, 26, 9, 0)),
                                                Availability(datetime(2023, 4, 28, 7, 0), datetime(2023, 4, 28, 9, 0)),
                                                Availability(datetime(2023, 4, 30, 7, 0), datetime(2023, 4, 30, 9, 0)),
                                                Availability(datetime(2023, 4, 6, 7, 0), datetime(2023, 4, 6, 9, 0)),
                                                Availability(datetime(2023, 4, 11, 7, 0), datetime(2023, 4, 11, 9, 0))],
                                                      {14:2, 15:2, 16:2, 17:2}, 12, 1, 1, 'coffee_company'))

employee_list.append(Employee('Isabel', 'Koster', [Availability(datetime(2023, 4, 6, 7, 0), datetime(2023, 4, 6, 9, 0)),
                                                Availability(datetime(2023, 4, 11, 7, 0), datetime(2023, 4, 11, 9, 0)),
                                                Availability(datetime(2023, 4, 19, 7, 0), datetime(2023, 4, 19, 9, 0)),
                                                Availability(datetime(2023, 4, 24, 7, 0), datetime(2023, 4, 24, 9, 0)),
                                                Availability(datetime(2023, 4, 27, 7, 0), datetime(2023, 4, 27, 9, 0)),
                                                Availability(datetime(2023, 4, 29, 7, 0), datetime(2023, 4, 29, 9, 0)),
                                                Availability(datetime(2023, 4, 3, 7, 0), datetime(2023, 4, 3, 9, 0)),
                                                Availability(datetime(2023, 4, 21, 7, 0), datetime(2023, 4, 21, 9, 0)),
                                                Availability(datetime(2023, 4, 26, 7, 0), datetime(2023, 4, 26, 9, 0))],
                                            {14:2, 15:2, 16:2, 17:2}, 11, 1, 1, 'coffee_company'))

employee_list.append(Employee('Alexandra', 'Offringa', [Availability(datetime(2023, 4, 7, 7, 0), datetime(2023, 4, 7, 9, 0)),
                                                Availability(datetime(2023, 4, 9, 7, 0), datetime(2023, 4, 9, 9, 0)),
                                                Availability(datetime(2023, 4, 17, 7, 0), datetime(2023, 4, 17, 9, 0)),
                                                Availability(datetime(2023, 4, 20, 7, 0), datetime(2023, 4, 20, 9, 0)),
                                                Availability(datetime(2023, 4, 25, 7, 0), datetime(2023, 4, 25, 9, 0)),
                                                Availability(datetime(2023, 4, 28, 7, 0), datetime(2023, 4, 28, 9, 0)),
                                                Availability(datetime(2023, 4, 10, 7, 0), datetime(2023, 4, 10, 9, 0)),
                                                Availability(datetime(2023, 4, 13, 7, 0), datetime(2023, 4, 13, 9, 0)),
                                                Availability(datetime(2023, 4, 18, 7, 0), datetime(2023, 4, 18, 9, 0)),
                                                Availability(datetime(2023, 4, 15, 7, 0), datetime(2023, 4, 15, 9, 0))],
                                             {14:0, 15:0, 16:0, 17:0}, 15.5, 1, 1, 'coffee_company'))

employee_list.append(Employee('Pim', 'Putman', [Availability(datetime(2023, 4, 4, 7, 0), datetime(2023, 4, 4, 9, 0)),
                                                Availability(datetime(2023, 4, 7, 7, 0), datetime(2023, 4, 7, 9, 0)),
                                                Availability(datetime(2023, 4, 9, 7, 0), datetime(2023, 4, 9, 9, 0)),
                                                Availability(datetime(2023, 4, 11, 7, 0), datetime(2023, 4, 11, 9, 0)),
                                                Availability(datetime(2023, 4, 14, 7, 0), datetime(2023, 4, 14, 9, 0)),
                                                Availability(datetime(2023, 4, 17, 7, 0), datetime(2023, 4, 17, 9, 0)),
                                                Availability(datetime(2023, 4, 21, 7, 0), datetime(2023, 4, 21, 9, 0)),
                                                Availability(datetime(2023, 4, 4, 7, 0), datetime(2023, 4, 4, 9, 0, 0)),
                                                Availability(datetime(2023, 4, 27, 7, 0), datetime(2023, 4, 27, 9, 0)),
                                                Availability(datetime(2023, 4, 30, 7, 0), datetime(2023, 4, 30, 9, 0)),
                                                Availability(datetime(2023, 4, 29, 7, 0), datetime(2023, 4, 29, 9, 0))],
                                            {14:0, 15:0, 16:0, 17:0}, 16.60, 1, 1, 'coffee_company'))

employee_list.append(Employee('Danaë', 'Verstegen', [Availability(datetime(2023, 4, 6, 7, 0), datetime(2023, 4, 6, 9, 0)),
                                                        Availability(datetime(2023, 4, 9, 7, 0), datetime(2023, 4, 9, 9, 0)),
                                                        Availability(datetime(2023, 4, 18, 7, 0), datetime(2023, 4, 18, 9, 0)),
                                                        Availability(datetime(2023, 4, 16, 7, 0), datetime(2023, 4, 16, 9, 0)),
                                                        Availability(datetime(2023, 4, 14, 7, 0), datetime(2023, 4, 14, 9, 0)),
                                                        Availability(datetime(2023, 4, 19, 7, 0), datetime(2023, 4, 19, 9, 0)),
                                                        Availability(datetime(2023, 4, 22, 7, 0), datetime(2023, 4, 22, 9, 0)),
                                                        Availability(datetime(2023, 4, 24, 7, 0), datetime(2023, 4, 24, 9, 0)),
                                                        Availability(datetime(2023, 4, 26, 7, 0), datetime(2023, 4, 26, 9, 0)),
                                                        Availability(datetime(2023, 4, 28, 7, 0), datetime(2023, 4, 28, 9, 0))],
                                               {14:2, 15:2, 16:2, 17:2}, 14, 1, 1, 'coffee_company'))

employee_list.append(Employee('Miranda', 'van Vuren', [Availability(datetime(2023, 4, 3, 7, 0), datetime(2023, 4, 3, 9, 0)),
                                                        Availability(datetime(2023, 4, 5, 7, 0), datetime(2023, 4, 5, 9, 0)),
                                                        Availability(datetime(2023, 4, 7, 7, 0), datetime(2023, 4, 7, 9, 0)),
                                                        Availability(datetime(2023, 4, 10, 7, 0), datetime(2023, 4, 10, 9, 0)),
                                                        Availability(datetime(2023, 4, 12, 7, 0), datetime(2023, 4, 12, 9, 0)),
                                                        Availability(datetime(2023, 4, 15, 7, 0), datetime(2023, 4, 15, 9, 0)),
                                                        Availability(datetime(2023, 4, 18, 7, 0), datetime(2023, 4, 18, 9, 0)),
                                                        Availability(datetime(2023, 4, 20, 7, 0), datetime(2023, 4, 20, 9, 0)),
                                                        Availability(datetime(2023, 4, 21, 7, 0), datetime(2023, 4, 21, 9, 0)),
                                                        Availability(datetime(2023, 4, 4, 7, 0), datetime(2023, 4, 4, 9, 0)),
                                                        Availability(datetime(2023, 4, 25, 7, 0), datetime(2023, 4, 25, 9, 0)),
                                                        Availability(datetime(2023, 4, 27, 7, 0), datetime(2023, 4, 27, 9, 0)),
                                                        Availability(datetime(2023, 4, 24, 7, 0), datetime(2023, 4, 24, 9, 0))],
                                               {14:2, 15:2, 16:2, 17:2}, 18, 1, 1, 'coffee_company'))

employee_list.append(Employee('Lulu', 'Wolff', [Availability(datetime(2023, 4, 27, 7, 0), datetime(2023, 4, 27, 9, 0)),
                                                Availability(datetime(2023, 4, 24, 7, 0), datetime(2023, 4, 24, 9, 0)),
                                                Availability(datetime(2023, 4, 22, 7, 0), datetime(2023, 4, 22, 9, 0)),
                                                Availability(datetime(2023, 4, 19, 7, 0), datetime(2023, 4, 19, 9, 0)),
                                                Availability(datetime(2023, 4, 17, 7, 0), datetime(2023, 4, 17, 9, 0)),
                                                Availability(datetime(2023, 4, 16, 7, 0), datetime(2023, 4, 16, 9, 0)),
                                                Availability(datetime(2023, 4, 13, 7, 0), datetime(2023, 4, 13, 9, 0)),
                                                Availability(datetime(2023, 4, 11, 7, 0), datetime(2023, 4, 11, 9, 0)),
                                                Availability(datetime(2023, 4, 8, 7, 0), datetime(2023, 4, 8, 9, 0)),
                                                Availability(datetime(2023, 4, 4, 7, 0), datetime(2023, 4, 4, 9, 0)),
                                                Availability(datetime(2023, 4, 4, 7, 0), datetime(2023, 4, 4, 9, 0)),
                                                Availability(datetime(2023, 4, 6, 7, 0), datetime(2023, 4, 6, 9, 0))],
                                           {14:0, 15:0, 16:0, 17:0}, 11, 1, 1, 'coffee_company'))

employee_list.append(Employee('Tamar', 'van der Zalm', [Availability(datetime(2023, 4, 6, 7, 0), datetime(2023, 4, 6, 9, 0)),
                                                        Availability(datetime(2023, 4, 20, 7, 0), datetime(2023, 4, 20, 9, 0)),
                                                        Availability(datetime(2023, 4, 23, 7, 0), datetime(2023, 4, 23, 9, 0)),
                                                        Availability(datetime(2023, 4, 8, 7, 0), datetime(2023, 4, 8, 9, 0)),
                                                        Availability(datetime(2023, 4, 10, 7, 0), datetime(2023, 4, 10, 9, 0)),
                                                        Availability(datetime(2023, 4, 13, 7, 0), datetime(2023, 4, 13, 9, 0)),
                                                        Availability(datetime(2023, 4, 16, 7, 0), datetime(2023, 4, 16, 9, 0)),
                                                        Availability(datetime(2023, 4, 17, 7, 0), datetime(2023, 4, 17, 9, 0)),
                                                        Availability(datetime(2023, 4, 25, 7, 0), datetime(2023, 4, 25, 9, 0)),
                                                        Availability(datetime(2023, 4, 29, 7, 0), datetime(2023, 4, 29, 9, 0)),
                                                        Availability(datetime(2023, 4, 30, 7, 0), datetime(2023, 4, 30, 9, 0))],
                                                  {14:2, 15:2, 16:2, 17:2}, 30, 1, 1, 'coffee_company'))

for day in range(3,31):
    shift_list.append(Shift(start=datetime(2023, 4, day, 7, 0),
                         end=datetime(2023, 4, day, 9, 0),
                         task=1, location=1))

"""
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

employee_list.append(Employee('Alexandra', 'Offringa', [],
                                                       {5:0, 1:0, 2:0, 3:0}, {5:1, 1:1, 2:1, 3:1}, 15.5, 1, [1], 'coffee_company'))

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
    shift_list.append(Shift(start=datetime(2023, 1, day, 7, 30),
                         end=datetime(2023, 1, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 1, day, 12, 30),
                         end=datetime(2023, 1, day, 18, 0),
                         task=1, location=1))

for day in range(1,6):
    shift_list.append(Shift(start=datetime(2023, 2, day, 7, 30),
                         end=datetime(2023, 2, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 2, day, 12, 30),
                         end=datetime(2023, 2, day, 18, 0),
                         task=1, location=1))
