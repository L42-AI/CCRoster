from datetime import date, time

from classes.representation.shift import ShiftData
from classes.representation.employee import Employee
from classes.representation.availabilty import Availability

employee_list: list[Employee] = []

employee_list.append(Employee('Emma', 'Deckers', [Availability(date=date(2023,1,30), start=time(0,0), end=time(23,59)),
                                                  Availability(date=date(2023,2,1), start=time(0,0), end=time(23,59)),
                                                  Availability(date=date(2023,2,2), start=time(0,0), end=time(23,59)),
                                                  Availability(date=date(2023,2,3), start=time(0,0), end=time(23,59))],
                                                  {0:2, 1:2, 2:2, 3:2}, 24, 1, 'Allround', 'coffee_company'))

employee_list.append(Employee('Soraya', 'van Geldere', [Availability(date=date(2023,1,30), start=time(0,0), end=time(23,59)),
                                                        Availability(date=date(2023,1,31), start=time(0,0), end=time(23,59)),
                                                        Availability(date=date(2023,2,1), start=time(0,0), end=time(23,59)),
                                                        Availability(date=date(2023,2,2), start=time(0,0), end=time(23,59))],
                                                        {0:4, 1:4, 2:4, 3:4}, 10, 1, 'Allround', 'coffee_company'))

employee_list.append(Employee("Sophie", "van 't Hullenaar", [Availability(date=date(2023,2,3), start=time(13,30), end=time(23,59)),
                                                             Availability(date=date(2023,2,4), start=time(0,0), end=time(23,59)),
                                                             Availability(date=date(2023,2,5), start=time(0,0), end=time(23,59))],
                                                             {0:2, 1:2, 2:2, 3:2}, 12, 1, 'Allround', 'coffee_company'))

employee_list.append(Employee('Isabella', 'Koster', [Availability(date=date(2023,1,30), start=time(7,30), end=time(18,00)),
                                                     Availability(date=date(2023,1,31), start=time(7,30), end=time(18,00)),
                                                     Availability(date=date(2023,2,4), start=time(8,30), end=time(13,30))],
                                                     {0:2, 1:2, 2:2, 3:2}, 11, 1, 'Allround', 'coffee_company'))

employee_list.append(Employee('Alexandra', 'Offringa', [],
                                                       {0:0, 1:0, 2:0, 3:0}, 15.5, 1, 'Allround', 'coffee_company'))

employee_list.append(Employee('Pim', 'Putman', [Availability(date=date(2023,1,30), start=time(0,0), end=time(14,00)),
                                                Availability(date=date(2023,1,31), start=time(0,0), end=time(23,59))],
                                                {0:0, 1:0, 2:0, 3:0}, 16.60, 1, 'Allround', 'coffee_company'))

employee_list.append(Employee('Danaë', 'Verstegen', [Availability(date=date(2023,1,30), start=time(0,0), end=time(23,59)),
                                                     Availability(date=date(2023,1,31), start=time(7,30), end=time(13,00)),
                                                     Availability(date=date(2023,2,5), start=time(8,30), end=time(13,30))],
                                                     {0:2, 1:2, 2:2, 3:2}, 14, 1, 'Allround', 'coffee_company'))

employee_list.append(Employee('Miranda', 'van Vuren', [Availability(date=date(2023,1,30), start=time(0,0), end=time(23,59)),
                                                       Availability(date=date(2023,1,31), start=time(0,0), end=time(23,59)),
                                                       Availability(date=date(2023,2,1), start=time(0,0), end=time(23,59)),
                                                       Availability(date=date(2023,2,2), start=time(0,0), end=time(23,59)),
                                                       Availability(date=date(2023,2,5), start=time(0,0), end=time(23,59))],
                                                       {0:2, 1:2, 2:2, 3:2}, 18, 1, 'Allround', 'coffee_company'))

employee_list.append(Employee('Lulu', 'Wolff', [Availability(date=date(2023,2,4), start=time(0,0), end=time(23,59))],
                                                {0:0, 1:0, 2:0, 3:0}, 11, 1, 'Allround', 'coffee_company'))

employee_list.append(Employee('Tamar', 'van der Zalm', [Availability(date=date(2023,2,1), start=time(13,0), end=time(23,59)),
                                                        Availability(date=date(2023,2,2), start=time(7,0), end=time(18,00))],
                                                        {0:2, 1:2, 2:2, 3:2}, 30, 1, 'Allround', 'coffee_company'))

shift_list: list[ShiftData] = []

shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,3), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,4), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,5), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,6), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,7), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,8), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,9), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,10), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,11), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,12), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,13), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,14), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,15), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,16), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,17), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,18), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,19), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,20), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,21), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,22), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,23), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,24), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,25), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,26), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,27), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,28), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,29), task=1, location=1))
shift_list.append(ShiftData(start=time(7), end=time(9), date=date(2023,4,30), task=1, location=1))