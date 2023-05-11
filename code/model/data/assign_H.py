from datetime import datetime

from model.representation.data_classes.availability import Availability
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

employee_list: list[Employee] = []
shift_list: list[Shift] = []

employee_list.append(Employee('Allumuah', ' ', [
    Availability(start=datetime(2023,5,18,7,0), end=datetime(2023,5,18,15,0)),
    Availability(start=datetime(2023,5,19,7,0), end=datetime(2023,5,19,15,0)),
    Availability(start=datetime(2023,5,20,8,14), end=datetime(2023,5,20,8,14)),
    Availability(start=datetime(2023,5,22,13,0), end=datetime(2023,5,2,18,3)),
    Availability(start=datetime(2023,5,25,7), end=datetime(2023,5,1,15)),
    Availability(start=datetime(2023,5,26,7), end=datetime(2023,5,3,15)),
    Availability(start=datetime(2023,5,27,8), end=datetime(2023,5,3,14)),
    ], {20:2, 21:3}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Lena', ' ', [

    Availability(start=datetime(2023,5,27,0), end=datetime(2023,5,27,23,59)),
    Availability(start=datetime(2023,5,28,0), end=datetime(2023,5,28,23,59)),
    ], {20:2, 21:2}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee("Beau", " ", [
    Availability(start=datetime(2023,5,27,0), end=datetime(2023,5,27,23,59)),
    Availability(start=datetime(2023,5,28,0), end=datetime(2023,5,28,23,59)),
    ], {20:1, 21:1}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Roos', ' ', [
    Availability(start=datetime(2023,5,15,0), end=datetime(2023,5,15,15,0)),
    Availability(start=datetime(2023,5,16,0), end=datetime(2023,5,16,15,0)),
    Availability(start=datetime(2023,5,17,0), end=datetime(2023,5,17,15,0)),
    Availability(start=datetime(2023,5,18,0), end=datetime(2023,5,18,15,0)),
    Availability(start=datetime(2023,5,19,0), end=datetime(2023,5,19,15,0)),
    Availability(start=datetime(2023,5,20,0), end=datetime(2023,5,20,15,0)),
    Availability(start=datetime(2023,5,22,0), end=datetime(2023,5,22,15,0)),
    Availability(start=datetime(2023,5,23,0), end=datetime(2023,5,23,15,0)),
    Availability(start=datetime(2023,5,24,0), end=datetime(2023,5,24,15,0)),
    Availability(start=datetime(2023,5,25,0), end=datetime(2023,5,25,15,0)),
    Availability(start=datetime(2023,5,26,0), end=datetime(2023,5,26,15,0)),
    Availability(start=datetime(2023,5,27,0), end=datetime(2023,5,27,15,0)),
    ], {20:3, 21:3}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Lodewijk', ' ', [
    Availability(start=datetime(2023,5,15,0), end=datetime(2023,5,15,23,59)),
    Availability(start=datetime(2023,5,16,0), end=datetime(2023,5,16,23,59)),
    Availability(start=datetime(2023,5,17,0), end=datetime(2023,5,17,23,59)),
    Availability(start=datetime(2023,5,18,0), end=datetime(2023,5,18,23,59)),
    Availability(start=datetime(2023,5,19,0), end=datetime(2023,5,19,23,59)),
    Availability(start=datetime(2023,5,23,0), end=datetime(2023,5,23,23,59)),
    Availability(start=datetime(2023,5,24,0), end=datetime(2023,5,24,23,59)),
    Availability(start=datetime(2023,5,25,0), end=datetime(2023,5,25,23,59)),
    Availability(start=datetime(2023,5,26,0), end=datetime(2023,5,26,23,59)),
    ], {20:3, 21:3}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Margot', ' ', [
    ], {20:2, 21:2}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Aimee', ' ', [
    Availability(start=datetime(2023,5,15,0), end=datetime(2023,5,15,23,59)),
    Availability(start=datetime(2023,5,18,0), end=datetime(2023,5,18,23,59)),
    Availability(start=datetime(2023,5,19,0), end=datetime(2023,5,19,23,59)),
    Availability(start=datetime(2023,5,22,0), end=datetime(2023,5,22,23,59)),
    Availability(start=datetime(2023,5,25,0), end=datetime(2023,5,25,23,59)),
    Availability(start=datetime(2023,5,26,0), end=datetime(2023,5,26,23,59)),
    ], {20:3, 21:3}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Alex', ' ', [
    Availability(start=datetime(2023,5,15,0), end=datetime(2023,5,15,23,59)),
    Availability(start=datetime(2023,5,16,0), end=datetime(2023,5,16,23,59)),
    Availability(start=datetime(2023,5,17,0), end=datetime(2023,5,17,23,59)),
    Availability(start=datetime(2023,5,18,0), end=datetime(2023,5,18,23,59)),
    Availability(start=datetime(2023,5,19,0), end=datetime(2023,5,19,23,59)),
    Availability(start=datetime(2023,5,20,0), end=datetime(2023,5,20,23,59)),
    Availability(start=datetime(2023,5,21,0), end=datetime(2023,5,21,23,59)),
    Availability(start=datetime(2023,5,22,0), end=datetime(2023,5,22,23,59)),
    Availability(start=datetime(2023,5,23,0), end=datetime(2023,5,23,23,59)),
    Availability(start=datetime(2023,5,24,0), end=datetime(2023,5,24,23,59)),
    Availability(start=datetime(2023,5,25,0), end=datetime(2023,5,25,23,59)),
    Availability(start=datetime(2023,5,26,0), end=datetime(2023,5,26,23,59)),
    Availability(start=datetime(2023,5,27,0), end=datetime(2023,5,27,23,59)),
    Availability(start=datetime(2023,5,28,0), end=datetime(2023,5,28,23,59)),
    ],{20:3, 21:3}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Sophie', ' ', [
    Availability(start=datetime(2023,5,15,0), end=datetime(2023,5,15,23,59)),
    Availability(start=datetime(2023,5,16,0), end=datetime(2023,5,16,23,59)),
    Availability(start=datetime(2023,5,20,0), end=datetime(2023,5,20,23,59)),
    Availability(start=datetime(2023,5,21,0), end=datetime(2023,5,21,23,59)),
    Availability(start=datetime(2023,5,22,0), end=datetime(2023,5,22,23,59)),
    Availability(start=datetime(2023,5,23,0), end=datetime(2023,5,23,23,59)),
    Availability(start=datetime(2023,5,27,0), end=datetime(2023,5,27,23,59)),
    Availability(start=datetime(2023,5,28,0), end=datetime(2023,5,28,23,59)),
    ], {20:2, 21:2}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Milou', ' ', [
    Availability(start=datetime(2023,5,16,7), end=datetime(2023,5,16,13)),
    Availability(start=datetime(2023,5,25,7), end=datetime(2023,5,25,13)),
    ], {20:1, 21:1}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Veere', ' ', [
    Availability(start=datetime(2023,5,18,0), end=datetime(2023,5,18,23,59)),
    Availability(start=datetime(2023,5,19,0), end=datetime(2023,5,19,23,59)),
    Availability(start=datetime(2023,5,20,0), end=datetime(2023,5,20,23,59)),
    Availability(start=datetime(2023,5,21,0), end=datetime(2023,5,21,23,59)),
    Availability(start=datetime(2023,5,25,0), end=datetime(2023,5,25,23,59)),
    Availability(start=datetime(2023,5,26,0), end=datetime(2023,5,26,23,59)),
    Availability(start=datetime(2023,5,27,0), end=datetime(2023,5,27,23,59)),
    Availability(start=datetime(2023,5,28,0), end=datetime(2023,5,28,23,59)),
    ], {20:1, 21:1}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Lieke', ' ', [
    ], {20:2, 21:2}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Britt', ' ', [
    Availability(start=datetime(2023,5,17,13), end=datetime(2023,5,17,23,59)),
    Availability(start=datetime(2023,5,18,0), end=datetime(2023,5,18,23,59)),
    Availability(start=datetime(2023,5,19,0), end=datetime(2023,5,19,23,59)),
    Availability(start=datetime(2023,5,20,0), end=datetime(2023,5,20,23,59)),
    Availability(start=datetime(2023,5,21,0), end=datetime(2023,5,21,23,59)),
    Availability(start=datetime(2023,5,22,0), end=datetime(2023,5,22,23,59)),
    Availability(start=datetime(2023,5,23,0), end=datetime(2023,5,23,13)),
    Availability(start=datetime(2023,5,24,13), end=datetime(2023,5,24,23,59)),
    Availability(start=datetime(2023,5,25,0), end=datetime(2023,5,25,13,0)),
    Availability(start=datetime(2023,5,26,0), end=datetime(2023,5,26,23,59)),
    Availability(start=datetime(2023,5,27,0), end=datetime(2023,5,27,23,59)),
], {20:3, 21:3}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Florine', ' ', [
    Availability(start=datetime(2023,5,15,0), end=datetime(2023,5,15,23,59)),
    Availability(start=datetime(2023,5,16,0), end=datetime(2023,5,16,23,59)),
    Availability(start=datetime(2023,5,18,0), end=datetime(2023,5,18,23,59)),
    Availability(start=datetime(2023,5,19,0), end=datetime(2023,5,19,23,59)),
    Availability(start=datetime(2023,5,20,0), end=datetime(2023,5,20,23,59)),
    Availability(start=datetime(2023,5,21,0), end=datetime(2023,5,21,23,59)),
    ], {20:4}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('Dumdum', 'Dummy', [], {20:2, 21:2}, 0, 100000, 1, [1], 'coffee_company'))

""" MAANDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 15, 7, 0),
    end=datetime(2023, 5, 15, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 15, 8, 0),
    end=datetime(2023, 5, 15, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 15, 9, 0),
    end=datetime(2023, 5, 15, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 15, 13, 0),
    end=datetime(2023, 5, 15, 18, 30),
    task=1, location=1))

""" DINSDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 16, 7, 0),
    end=datetime(2023, 5, 16, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 16, 9, 0),
    end=datetime(2023, 5, 16, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 16, 13, 0),
    end=datetime(2023, 5, 16, 18, 30),
    task=1, location=1))

""" WOENSDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 17, 7, 0),
    end=datetime(2023, 5, 17, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 17, 9, 0),
    end=datetime(2023, 5, 17, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 17, 13, 0),
    end=datetime(2023, 5, 17, 18, 30),
    task=1, location=1))

""" DONDERDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 18, 7, 0),
    end=datetime(2023, 5, 18, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 18, 9, 0),
    end=datetime(2023, 5, 18, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 18, 13, 0),
    end=datetime(2023, 5, 18, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 18, 13, 0),
    end=datetime(2023, 5, 18, 18, 30),
    task=1, location=1))

""" VRIJDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 19, 7, 0),
    end=datetime(2023, 5, 19, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 19, 9, 0),
    end=datetime(2023, 5, 19, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 19, 13, 0),
    end=datetime(2023, 5, 19, 18, 30),
    task=1, location=1))

""" ZATERDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 20, 8, 0),
    end=datetime(2023, 5, 20, 12, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 20, 9, 0),
    end=datetime(2023, 5, 20, 14, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 20, 12, 0),
    end=datetime(2023, 5, 20, 18, 00),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 20, 14, 0),
    end=datetime(2023, 5, 20, 19, 30),
    task=1, location=1))

""" ZONDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 21, 8, 0),
    end=datetime(2023, 5, 21, 12, 30),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 21, 9, 0),
    end=datetime(2023, 5, 21, 14, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 21, 9, 0),
    end=datetime(2023, 5, 21, 15, 00),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 21, 13, 0),
    end=datetime(2023, 5, 21, 18, 30),
    task=1, location=1))

""" MAANDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 22, 7, 0),
    end=datetime(2023, 5, 22, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 22, 8, 0),
    end=datetime(2023, 5, 22, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 22, 9, 0),
    end=datetime(2023, 5, 22, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 22, 13, 0),
    end=datetime(2023, 5, 22, 18, 30),
    task=1, location=1))

""" DINSDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 23, 7, 0),
    end=datetime(2023, 5, 23, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 23, 9, 0),
    end=datetime(2023, 5, 23, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 23, 13, 0),
    end=datetime(2023, 5, 23, 18, 30),
    task=1, location=1))

""" WOENSDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 24, 7, 0),
    end=datetime(2023, 5, 24, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 24, 9, 0),
    end=datetime(2023, 5, 24, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 24, 13, 0),
    end=datetime(2023, 5, 24, 18, 30),
    task=1, location=1))

""" DONDERDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 25, 7, 0),
    end=datetime(2023, 5, 25, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 25, 9, 0),
    end=datetime(2023, 5, 25, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 25, 13, 0),
    end=datetime(2023, 5, 25, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 25, 13, 0),
    end=datetime(2023, 5, 25, 18, 30),
    task=1, location=1))

""" VRIJDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 26, 7, 0),
    end=datetime(2023, 5, 26, 13, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 26, 9, 0),
    end=datetime(2023, 5, 26, 15, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 26, 13, 0),
    end=datetime(2023, 5, 26, 18, 30),
    task=1, location=1))

""" ZATERDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 27, 8, 0),
    end=datetime(2023, 5, 27, 12, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 27, 9, 0),
    end=datetime(2023, 5, 27, 14, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 27, 12, 0),
    end=datetime(2023, 5, 27, 18, 00),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 27, 14, 0),
    end=datetime(2023, 5, 27, 19, 30),
    task=1, location=1))

""" ZONDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 28, 8, 0),
    end=datetime(2023, 5, 28, 12, 30),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 28, 9, 0),
    end=datetime(2023, 5, 28, 14, 0),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 28, 9, 0),
    end=datetime(2023, 5, 28, 15, 00),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 28, 13, 0),
    end=datetime(2023, 5, 28, 18, 30),
    task=1, location=1))

for id_, employee in enumerate(employee_list):
    employee.id = id_

for id_, shift in enumerate(shift_list):
    shift.id = id_

