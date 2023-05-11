from datetime import datetime

from model.representation.data_classes.availability import Availability
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

employee_list: list[Employee] = []
shift_list: list[Shift] = []

employee_list.append(Employee('Emma', 'Deckers', [Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,23,59)),
                                                  Availability(start=datetime(2023, 5,1,0), end=datetime(2023, 5,1,23,59)),
                                                  Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)),
                                                  Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)),
                                                  Availability(start=datetime(2023, 5,1,13), end=datetime(2023, 5,1,23,59)),
                                                  Availability(start=datetime(2023, 5,3,0), end=datetime(2023, 5,3,23,59))],
                                                  {5:2, 1:2, 2:2, 3:2}, 4, 240, 1, [1], 1)) # location 1 is coffee comp for development

employee_list.append(Employee('Soraya', 'van Geldere', [Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,23,59)),
                                                        Availability(start=datetime(2023, 4,30,0), end=datetime(2023, 4,30,23,59)),
                                                        Availability(start=datetime(2023, 5,1,0), end=datetime(2023, 5,1,23,59)),
                                                        Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)), ],
                                                        {5:2, 1:2, 2:2, 3:2}, 4, 3, 1, [1], 1)) # location 1 is coffee comp for development

employee_list.append(Employee("Sophie", "van 't Hullenaar", [Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,23,59)),
                                                        Availability(start=datetime(2023, 4,30,0), end=datetime(2023, 4,30,23,59)),
                                                        Availability(start=datetime(2023, 5,1,0), end=datetime(2023, 5,1,23,59)),
                                                        Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)),
                                                        Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,23,59)),
                                                        Availability(start=datetime(2023, 5,3,13,3), end=datetime(2023, 5,3,23,59)),
                                                        Availability(start=datetime(2023, 5,4,0), end=datetime(2023, 5,4,23,59)),
                                                        Availability(start=datetime(2023, 5,5,0), end=datetime(2023, 5,5,23,59))],
                                                             {5:2, 1:2, 2:2, 3:2}, 4, 12, 1, [1], 1)) # location 1 is coffee comp for development

employee_list.append(Employee('Isabella', 'Koster', [Availability(start=datetime(2023, 5,3,13,3), end=datetime(2023, 5,3,23,59)),
                                                             Availability(start=datetime(2023, 5,4,0), end=datetime(2023, 5,4,23,59)),
                                                             Availability(start=datetime(2023, 5,5,0), end=datetime(2023, 5,5,23,59)),
                                                    Availability(start=datetime(2023, 4,29,7,3), end=datetime(2023, 4,29,18,00)),
                                                     Availability(start=datetime(2023, 4,30,7,3), end=datetime(2023, 4,30,18,00)),
                                                     Availability(start=datetime(2023, 5,4,8,3), end=datetime(2023, 5,4,13,30))],
                                                     {5:2, 1:2, 2:2, 3:2}, 4, 11, 1, [1], 1)) # location 1 is coffee comp for development

employee_list.append(Employee('Alexandra', 'Offringa', [Availability(start=datetime(2023, 5,3,0), end=datetime(2023, 5,3,23,59))],
                                                       {5:1, 1:0, 2:0, 3:0}, 4, 200.5, 1, [1], 1)) # location 1 is coffee comp for development

employee_list.append(Employee('Pim', 'Putman', [Availability(start=datetime(2023, 5,3,0), end=datetime(2023, 5,3,23,59)),
                                                Availability(start=datetime(2023, 5,1,0), end=datetime(2023, 5,1,23,59)),
                                                Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)),
                                                Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,23,59)),
                                                Availability(start=datetime(2023, 5,1,0), end=datetime(2023, 5,1,23,59)),
                                                Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,14)),
                                                Availability(start=datetime(2023, 4,30,0), end=datetime(2023, 4,30,23,59))],
                                                {5:2, 1:0, 2:0, 3:0}, 4, 16.60, 1, [1], 1)) # location 1 is coffee comp for development

employee_list.append(Employee('Danaë', 'Verstegen', [Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,23,59)),
                                                    Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,23,59)),
                                                    Availability(start=datetime(2023, 5,1,0), end=datetime(2023, 5,1,23,59)),
                                                    Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,14)),
                                                     Availability(start=datetime(2023, 4,30,7,3), end=datetime(2023, 4,30,13,00)),
                                                     Availability(start=datetime(2023, 5,5,8,3), end=datetime(2023, 5,5,13,30))],
                                                     {5:2, 1:2, 2:2, 3:2}, 4, 14, 1, [1], 1)) # location 1 is coffee comp for development

employee_list.append(Employee('Miranda', 'van Vuren', [Availability(start=datetime(2023, 4,29,0), end=datetime(2023, 4,29,23,59)),
                                                    Availability(start=datetime(2023, 4,30,7,3), end=datetime(2023, 4,30,13,00)),
                                                     Availability(start=datetime(2023, 5,5,8,3), end=datetime(2023, 5,5,13,30)),
                                                       Availability(start=datetime(2023, 4,30,0), end=datetime(2023, 4,30,23,59)),
                                                       Availability(start=datetime(2023, 5,1,0), end=datetime(2023, 5,1,23,59)),
                                                       Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)),
                                                       Availability(start=datetime(2023, 5,5,0), end=datetime(2023, 5,5,23,59))],
                                                       {5:2, 1:2, 2:2, 3:2}, 4, 18, 1, [1], 1)) # location 1 is coffee comp for development

employee_list.append(Employee('Lulu', 'Wolff', [Availability(start=datetime(2023, 5,4,0), end=datetime(2023, 5,4,23,59))],
                                                {5:1, 1:0, 2:0, 3:0}, 4, 1, 1, [1], 1)) # location 1 is coffee comp for development

employee_list.append(Employee('Tamar', 'van der Zalm', [Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)),
                                                        Availability(start=datetime(2023, 4,30,0), end=datetime(2023, 4,30,23,59)),
                                                       Availability(start=datetime(2023, 5,1,0), end=datetime(2023, 5,1,23,59)),
                                                       Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)),
                                                       Availability(start=datetime(2023, 5,1,13), end=datetime(2023, 5,1,23,59)),
                                                        Availability(start=datetime(2023, 5,2,7), end=datetime(2023, 5,2,18,00))],
                                                        {5:2, 1:2, 2:2, 3:2}, 4, 50, 1, [1], 1)) # location 1 is coffee comp for development
employee_list.append(Employee('Dumdum', 'Dummy', [Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)),
                                                        Availability(start=datetime(2023, 4,30,0), end=datetime(2023, 4,30,23,59)),
                                                       Availability(start=datetime(2023, 5,1,0), end=datetime(2023, 5,1,23,59)),
                                                       Availability(start=datetime(2023, 5,2,0), end=datetime(2023, 5,2,23,59)),
                                                       Availability(start=datetime(2023, 5,1,13), end=datetime(2023, 5,1,23,59)),
                                                        Availability(start=datetime(2023, 5,2,7), end=datetime(2023, 5,2,18,00))],
                                                        {5:2, 1:2, 2:2, 3:2}, 0, 100000, 1, [1], 1)) # location 1 is coffee comp for development


# short shifts
for day in range(29,31):
    shift_list.append(Shift(start=datetime(2023, 4, day, 10, 30),
                         end=datetime(2023, 4, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 4, day, 13, 30),
                         end=datetime(2023, 4, day, 18, 0),
                         task=1, location=1))
    
# medium shifts
for day in range(1,3):
    shift_list.append(Shift(start=datetime(2023, 5, day, 9, 0),
                         end=datetime(2023, 5, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 5, day, 14, 0),
                         end=datetime(2023, 5, day, 18, 0),
                         task=1, location=1))
    
# long shifts
for day in range(4,6):
    shift_list.append(Shift(start=datetime(2023, 5, day, 7, 30),
                         end=datetime(2023, 5, day, 13, 0),
                         task=1, location=1))
    shift_list.append(Shift(start=datetime(2023, 5, day, 12, 30),
                         end=datetime(2023, 5, day, 18, 0),
                         task=1, location=1))

for id_, employee in enumerate(employee_list):
    employee.id = id_

for id_, shift in enumerate(shift_list):
    shift.id = id_