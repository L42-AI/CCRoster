import datetime

from classes.representation.shift import ShiftData
from classes.representation.employee import Employee


employee_list: list[Employee] = []

employee_list.append(Employee('Emma', 'Deckers', [(datetime.datetime(2023, 4, 3, 7, 0), datetime.datetime(2023, 4, 3, 9, 0)),
                                                (datetime.datetime(2023, 4, 10, 7, 0), datetime.datetime(2023, 4, 10, 9, 0)),
                                                (datetime.datetime(2023, 4, 15, 7, 0), datetime.datetime(2023, 4, 15, 9, 0)),
                                                (datetime.datetime(2023, 4, 30, 7, 0), datetime.datetime(2023, 4, 30, 9, 0)),
                                                (datetime.datetime(2023, 4, 22, 7, 0), datetime.datetime(2023, 4, 22, 9, 0)),
                                                (datetime.datetime(2023, 4, 13, 7, 0), datetime.datetime(2023, 4, 13, 9, 0)),
                                                (datetime.datetime(2023, 4, 17, 7, 0), datetime.datetime(2023, 4, 17, 9, 0)),
                                                (datetime.datetime(2023, 4, 12, 7, 0), datetime.datetime(2023, 4, 12, 9, 0))],
                                             {14:2, 15:2, 16:2, 17:2}, 24, 1, 'everything', 'coffee_company'))

employee_list.append(Employee('Soraya', 'van Geldere', [(datetime.datetime(2023, 4, 13, 7, 0), datetime.datetime(2023, 4, 13, 9, 0)),
                                                (datetime.datetime(2023, 4, 12, 7, 0), datetime.datetime(2023, 4, 12, 9, 0)),
                                                (datetime.datetime(2023, 4, 16, 7, 0), datetime.datetime(2023, 4, 16, 9, 0)),
                                                (datetime.datetime(2023, 4, 29, 7, 0), datetime.datetime(2023, 4, 29, 9, 0)),
                                                (datetime.datetime(2023, 4, 23, 7, 0), datetime.datetime(2023, 4, 23, 9, 0)),
                                                (datetime.datetime(2023, 4, 3, 7, 0), datetime.datetime(2023, 4, 3, 9, 0)),
                                                (datetime.datetime(2023, 4, 17, 7, 0), datetime.datetime(2023, 4, 17, 9, 0)),
                                                (datetime.datetime(2023, 4, 8, 7, 0), datetime.datetime(2023, 4, 8, 9, 0))],
                                                 {14:4, 15:4, 16:4, 17:4}, 10, 1, 'everything', 'coffee_company'))

employee_list.append(Employee("Sophie", "van 't Hullenaar", [(datetime.datetime(2023, 4, 3, 7, 0), datetime.datetime(2023, 4, 3, 9, 0)),
                                                (datetime.datetime(2023, 4, 8, 7, 0), datetime.datetime(2023, 4, 8, 9, 0)),
                                                (datetime.datetime(2023, 4, 23, 7, 0), datetime.datetime(2023, 4, 23, 9, 0)),
                                                (datetime.datetime(2023, 4, 14, 7, 0), datetime.datetime(2023, 4, 14, 9, 0)),
                                                (datetime.datetime(2023, 4, 12, 7, 0), datetime.datetime(2023, 4, 12, 9, 0)),
                                                (datetime.datetime(2023, 4, 26, 7, 0), datetime.datetime(2023, 4, 26, 9, 0)),
                                                (datetime.datetime(2023, 4, 28, 7, 0), datetime.datetime(2023, 4, 28, 9, 0)),
                                                (datetime.datetime(2023, 4, 30, 7, 0), datetime.datetime(2023, 4, 30, 9, 0)),
                                                (datetime.datetime(2023, 4, 6, 7, 0), datetime.datetime(2023, 4, 6, 9, 0)),
                                                (datetime.datetime(2023, 4, 11, 7, 0), datetime.datetime(2023, 4, 11, 9, 0))],
                                                      {14:2, 15:2, 16:2, 17:2}, 12, 1, 'everything', 'coffee_company'))

employee_list.append(Employee('Isabel', 'Koster', [(datetime.datetime(2023, 4, 6, 7, 0), datetime.datetime(2023, 4, 6, 9, 0)),
                                                (datetime.datetime(2023, 4, 11, 7, 0), datetime.datetime(2023, 4, 11, 9, 0)),
                                                (datetime.datetime(2023, 4, 19, 7, 0), datetime.datetime(2023, 4, 19, 9, 0)),
                                                (datetime.datetime(2023, 4, 24, 7, 0), datetime.datetime(2023, 4, 24, 9, 0)),
                                                (datetime.datetime(2023, 4, 27, 7, 0), datetime.datetime(2023, 4, 27, 9, 0)),
                                                (datetime.datetime(2023, 4, 29, 7, 0), datetime.datetime(2023, 4, 29, 9, 0)),
                                                (datetime.datetime(2023, 4, 3, 7, 0), datetime.datetime(2023, 4, 3, 9, 0)),
                                                (datetime.datetime(2023, 4, 21, 7, 0), datetime.datetime(2023, 4, 21, 9, 0)),
                                                (datetime.datetime(2023, 4, 26, 7, 0), datetime.datetime(2023, 4, 26, 9, 0))],
                                            {14:2, 15:2, 16:2, 17:2}, 11, 1, 'everything', 'coffee_company'))

employee_list.append(Employee('Alexandra', 'Offringa', [(datetime.datetime(2023, 4, 7, 7, 0), datetime.datetime(2023, 4, 7, 9, 0)),
                                                (datetime.datetime(2023, 4, 9, 7, 0), datetime.datetime(2023, 4, 9, 9, 0)),
                                                (datetime.datetime(2023, 4, 17, 7, 0), datetime.datetime(2023, 4, 17, 9, 0)),
                                                (datetime.datetime(2023, 4, 20, 7, 0), datetime.datetime(2023, 4, 20, 9, 0)),
                                                (datetime.datetime(2023, 4, 25, 7, 0), datetime.datetime(2023, 4, 25, 9, 0)),
                                                (datetime.datetime(2023, 4, 28, 7, 0), datetime.datetime(2023, 4, 28, 9, 0)),
                                                (datetime.datetime(2023, 4, 10, 7, 0), datetime.datetime(2023, 4, 10, 9, 0)),
                                                (datetime.datetime(2023, 4, 13, 7, 0), datetime.datetime(2023, 4, 13, 9, 0)),
                                                (datetime.datetime(2023, 4, 18, 7, 0), datetime.datetime(2023, 4, 18, 9, 0)),
                                                (datetime.datetime(2023, 4, 15, 7, 0), datetime.datetime(2023, 4, 15, 9, 0))],
                                             {14:0, 15:0, 16:0, 17:0}, 15.5, 1, 'everything', 'coffee_company'))

employee_list.append(Employee('Pim', 'Putman', [(datetime.datetime(2023, 4, 4, 7), datetime.datetime(2023, 4, 4, 9)),
                                                (datetime.datetime(2023, 4, 7, 7), datetime.datetime(2023, 4, 7, 9)),
                                                (datetime.datetime(2023, 4, 9, 7), datetime.datetime(2023, 4, 9, 9)),
                                                (datetime.datetime(2023, 4, 11, 7), datetime.datetime(2023, 4, 11, 9)),
                                                (datetime.datetime(2023, 4, 14, 7), datetime.datetime(2023, 4, 14, 9)),
                                                (datetime.datetime(2023, 4, 17, 7), datetime.datetime(2023, 4, 17, 9)),
                                                (datetime.datetime(2023, 4, 21, 7), datetime.datetime(2023, 4, 21, 9)),
                                                (datetime.datetime(2023, 4, 4, 7, 0), datetime.datetime(2023, 4, 4, 9, 0)),
                                                (datetime.datetime(2023, 4, 27, 7), datetime.datetime(2023, 4, 27, 9)),
                                                (datetime.datetime(2023, 4, 30, 7), datetime.datetime(2023, 4, 30, 9)),
                                                (datetime.datetime(2023, 4, 29, 7), datetime.datetime(2023, 4, 29, 9))],
                                            {14:0, 15:0, 16:0, 17:0}, 16.60, 1, 'everything', 'coffee_company'))


employee_list.append(Employee('Danaë', 'Verstegen', [(datetime.datetime(2023, 4, 6, 7), datetime.datetime(2023, 4, 6, 9)),
                                                        (datetime.datetime(2023, 4, 9, 7), datetime.datetime(2023, 4, 9, 9)),
                                                        (datetime.datetime(2023, 4, 18, 7), datetime.datetime(2023, 4, 18, 9)),
                                                        (datetime.datetime(2023, 4, 16, 7), datetime.datetime(2023, 4, 16, 9)),
                                                        (datetime.datetime(2023, 4, 14, 7), datetime.datetime(2023, 4, 14, 9)),
                                                        (datetime.datetime(2023, 4, 19, 7), datetime.datetime(2023, 4, 19, 9)),
                                                        (datetime.datetime(2023, 4, 22, 7), datetime.datetime(2023, 4, 22, 9)),
                                                        (datetime.datetime(2023, 4, 24, 7), datetime.datetime(2023, 4, 24, 9)),
                                                        (datetime.datetime(2023, 4, 26, 7), datetime.datetime(2023, 4, 26, 9)),
                                                        (datetime.datetime(2023, 4, 28, 7), datetime.datetime(2023, 4, 28, 9))],
                                               {14:2, 15:2, 16:2, 17:2}, 14, 1, 'everything', 'coffee_company'))

employee_list.append(Employee('Miranda', 'van Vuren', [(datetime.datetime(2023, 4, 3, 7), datetime.datetime(2023, 4, 3, 9)),
                                                        (datetime.datetime(2023, 4, 5, 7), datetime.datetime(2023, 4, 5, 9)),
                                                        (datetime.datetime(2023, 4, 7, 7), datetime.datetime(2023, 4, 7, 9)),
                                                        (datetime.datetime(2023, 4, 10, 7), datetime.datetime(2023, 4, 10, 9)),
                                                        (datetime.datetime(2023, 4, 12, 7), datetime.datetime(2023, 4, 12, 9)),
                                                        (datetime.datetime(2023, 4, 15, 7), datetime.datetime(2023, 4, 15, 9)),
                                                        (datetime.datetime(2023, 4, 18, 7), datetime.datetime(2023, 4, 18, 9)),
                                                        (datetime.datetime(2023, 4, 20, 7), datetime.datetime(2023, 4, 20, 9)),
                                                        (datetime.datetime(2023, 4, 21, 7), datetime.datetime(2023, 4, 21, 9)),
                                                        (datetime.datetime(2023, 4, 4, 7, 0), datetime.datetime(2023, 4, 4, 9, 0)),
                                                        (datetime.datetime(2023, 4, 25, 7), datetime.datetime(2023, 4, 25, 9)),
                                                        (datetime.datetime(2023, 4, 27, 7, 0), datetime.datetime(2023, 4, 27, 9, 0)),
                                                (datetime.datetime(2023, 4, 24, 7, 0), datetime.datetime(2023, 4, 24, 9, 0))],
                                               {14:2, 15:2, 16:2, 17:2}, 18, 1, 'everything', 'coffee_company'))

employee_list.append(Employee('Lulu', 'Wolff', [(datetime.datetime(2023, 4, 27, 7, 0), datetime.datetime(2023, 4, 27, 9, 0)),
                                                (datetime.datetime(2023, 4, 24, 7, 0), datetime.datetime(2023, 4, 24, 9, 0)),
                                                (datetime.datetime(2023, 4, 22, 7, 0), datetime.datetime(2023, 4, 22, 9, 0)),
                                                (datetime.datetime(2023, 4, 19, 7, 0), datetime.datetime(2023, 4, 19, 9, 0)),
                                                (datetime.datetime(2023, 4, 17, 7, 0), datetime.datetime(2023, 4, 17, 9, 0)),
                                                (datetime.datetime(2023, 4, 16, 7, 0), datetime.datetime(2023, 4, 16, 9, 0)),
                                                (datetime.datetime(2023, 4, 13, 7, 0), datetime.datetime(2023, 4, 13, 9, 0)),
                                                (datetime.datetime(2023, 4, 11, 7, 0), datetime.datetime(2023, 4, 11, 9, 0)),
                                                (datetime.datetime(2023, 4, 8, 7, 0), datetime.datetime(2023, 4, 8, 9, 0)),
                                                (datetime.datetime(2023, 4, 4, 7, 0), datetime.datetime(2023, 4, 4, 9, 0)),
                                                (datetime.datetime(2023, 4, 4, 7, 0), datetime.datetime(2023, 4, 4, 9, 0)),
                                                (datetime.datetime(2023, 4, 6, 7, 0), datetime.datetime(2023, 4, 6, 9, 0))],
                                           {14:0, 15:0, 16:0, 17:0}, 11, 1, 'everything', 'coffee_company'))

employee_list.append(Employee('Tamar', 'van der Zalm', [(datetime.datetime(2023, 4, 6, 7, 0), datetime.datetime(2023, 4, 6, 9, 0)),
                                                        (datetime.datetime(2023, 4, 20, 7, 0), datetime.datetime(2023, 4, 20, 9, 0)),
                                                        (datetime.datetime(2023, 4, 23, 7, 0), datetime.datetime(2023, 4, 23, 9, 0)),
                                                        (datetime.datetime(2023, 4, 8, 7, 0), datetime.datetime(2023, 4, 8, 9, 0)),
                                                        (datetime.datetime(2023, 4, 10, 7, 0), datetime.datetime(2023, 4, 10, 9, 0)),
                                                        (datetime.datetime(2023, 4, 13, 7, 0), datetime.datetime(2023, 4, 13, 9, 0)),
                                                        (datetime.datetime(2023, 4, 16, 7, 0), datetime.datetime(2023, 4, 16, 9, 0)),
                                                        (datetime.datetime(2023, 4, 17, 7, 0), datetime.datetime(2023, 4, 17, 9, 0)),
                                                        (datetime.datetime(2023, 4, 25, 7, 0), datetime.datetime(2023, 4, 25, 9, 0)),
                                                        (datetime.datetime(2023, 4, 29, 7, 0), datetime.datetime(2023, 4, 29, 9, 0)),
                                                        (datetime.datetime(2023, 4, 30, 7, 0), datetime.datetime(2023, 4, 30, 9, 0))],
                                                  {14:2, 15:2, 16:2, 17:2}, 30, 1, 'everything', 'coffee_company'))

shift_list: list[ShiftData] = []

shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 3, 7, 0), end=datetime.datetime(2023, 4, 3, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 4, 7, 0), end=datetime.datetime(2023, 4, 4, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 5, 7, 0), end=datetime.datetime(2023, 4, 5, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 6, 7, 0), end=datetime.datetime(2023, 4, 6, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 7, 7, 0), end=datetime.datetime(2023, 4, 7, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 8, 7, 0), end=datetime.datetime(2023, 4, 8, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 9, 7, 0), end=datetime.datetime(2023, 4, 9, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 10, 7, 0), end=datetime.datetime(2023, 4, 10, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 11, 7, 0), end=datetime.datetime(2023, 4, 11, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 12, 7, 0), end=datetime.datetime(2023, 4, 12, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 13, 7, 0), end=datetime.datetime(2023, 4, 13, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 14, 7, 0), end=datetime.datetime(2023, 4, 14, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 15, 7, 0), end=datetime.datetime(2023, 4, 15, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 16, 7, 0), end=datetime.datetime(2023, 4, 16, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 17, 7, 0), end=datetime.datetime(2023, 4, 17, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 18, 7, 0), end=datetime.datetime(2023, 4, 18, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 19, 7, 0), end=datetime.datetime(2023, 4, 19, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 20, 7, 0), end=datetime.datetime(2023, 4, 20, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 21, 7, 0), end=datetime.datetime(2023, 4, 21, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 22, 7, 0), end=datetime.datetime(2023, 4, 22, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 23, 7, 0), end=datetime.datetime(2023, 4, 23, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 24, 7, 0), end=datetime.datetime(2023, 4, 24, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 25, 7, 0), end=datetime.datetime(2023, 4, 25, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 26, 7, 0), end=datetime.datetime(2023, 4, 26, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 27, 7, 0), end=datetime.datetime(2023, 4, 27, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 28, 7, 0), end=datetime.datetime(2023, 4, 28, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 29, 7, 0), end=datetime.datetime(2023, 4, 29, 9, 0), task=1, location=1))
shift_list.append(ShiftData(start=datetime.datetime(2023, 4, 30, 7, 0), end=datetime.datetime(2023, 4, 30, 9, 0), task=1, location=1))