from datetime import datetime

from model.representation.data_classes.availability import Availability
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

employee_list: list[Employee] = []
shift_list: list[Shift] = []

employee_list.append(Employee('1', ' ', [
    Availability(start=datetime(2023,5,29,9,0), end=datetime(2023,5,29,13,0)),
    Availability(start=datetime(2023,5,30,15,0), end=datetime(2023,5,30,17,0)),
    Availability(start=datetime(2023,5,31,0), end=datetime(2023,5,31,23,59)),
    Availability(start=datetime(2023,6,2,13,0), end=datetime(2023,6,2,18,0)),
    ], {22:4}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('2', ' ', [
    Availability(start=datetime(2023,5,29,0), end=datetime(2023,5,29,23,59)),
    Availability(start=datetime(2023,5,30,0), end=datetime(2023,5,30,23,59)),
    Availability(start=datetime(2023,6,1,11), end=datetime(2023,6,1,13)),
    Availability(start=datetime(2023,6,2,11), end=datetime(2023,6,2,13)),
    Availability(start=datetime(2023,6,4,0), end=datetime(2023,6,4,23,59)),
    ], {22:4}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee("3", " ", [
    Availability(start=datetime(2023,5,29,13), end=datetime(2023,5,29,18)),
    Availability(start=datetime(2023,5,31,9), end=datetime(2023,5,31,13)),
    Availability(start=datetime(2023,6,1,13), end=datetime(2023,6,1,17)),
    Availability(start=datetime(2023,6,2,13), end=datetime(2023,6,2,17)),
    Availability(start=datetime(2023,6,3,9), end=datetime(2023,6,3,13)),
    ], {22:5}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('4', ' ', [
    Availability(start=datetime(2023,5,29,15), end=datetime(2023,5,29,17)),
    Availability(start=datetime(2023,6,1,13), end=datetime(2023,6,1,15)),
    Availability(start=datetime(2023,6,4,0), end=datetime(2023,6,4,23,59)),
    ], {22:2}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('5', ' ', [
    Availability(start=datetime(2023,5,29,11), end=datetime(2023,5,29,17)),
    Availability(start=datetime(2023,5,31,0), end=datetime(2023,5,31,23,59)),
    Availability(start=datetime(2023,6,3,0), end=datetime(2023,6,3,23,59)),
    ], {22:3}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('6', ' ', [
    Availability(start=datetime(2023,5,30,13), end=datetime(2023,5,30,18)),
    Availability(start=datetime(2023,5,31,13), end=datetime(2023,5,31,17)),
    Availability(start=datetime(2023,6,3,0), end=datetime(2023,6,3,23,59)),
    Availability(start=datetime(2023,6,4,9), end=datetime(2023,6,4,13)),
    ], {22:3}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('7', ' ', [
    Availability(start=datetime(2023,6,1,0), end=datetime(2023,6,1,23,59)),
    Availability(start=datetime(2023,6,2,9), end=datetime(2023,6,2,13)),
    Availability(start=datetime(2023,6,4,9), end=datetime(2023,6,4,15)),
    ],{22:3}, 1, 10, 1, [1], 'coffee_company'))

employee_list.append(Employee('8', ' ', [
    Availability(start=datetime(2023,6,3,9), end=datetime(2023,6,3,13)),
    ], {22:1}, 1, 10, 1, [1], 'coffee_company'))

""" MAANDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 29, 9),
    end=datetime(2023, 5, 29, 13),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 29, 13),
    end=datetime(2023, 5, 29, 18),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 29, 13),
    end=datetime(2023, 5, 29, 15),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 29, 15),
    end=datetime(2023, 5, 29, 17),
    task=1, location=1))

""" DINSDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 30, 9),
    end=datetime(2023, 5, 30, 13),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 30, 13),
    end=datetime(2023, 5, 30, 18),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 30, 15),
    end=datetime(2023, 5, 30, 17),
    task=1, location=1))

""" WOENSDAG """

shift_list.append(Shift(
    start=datetime(2023, 5, 31, 9),
    end=datetime(2023, 5, 31, 13),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 31, 13),
    end=datetime(2023, 5, 31, 18),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 31, 11),
    end=datetime(2023, 5, 31, 13),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 5, 31, 13),
    end=datetime(2023, 5, 31, 15),
    task=1, location=1))

""" DONDERDAG """

shift_list.append(Shift(
    start=datetime(2023, 6, 1, 13),
    end=datetime(2023, 6, 1, 18),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 1, 11),
    end=datetime(2023, 6, 1, 13),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 1, 13),
    end=datetime(2023, 6, 1, 15),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 1, 15),
    end=datetime(2023, 6, 1, 17),
    task=1, location=1))

""" VRIJDAG """

shift_list.append(Shift(
    start=datetime(2023, 6, 2, 9),
    end=datetime(2023, 6, 2, 13),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 2, 13),
    end=datetime(2023, 6, 2, 18),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 2, 11),
    end=datetime(2023, 6, 2, 13),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 2, 15),
    end=datetime(2023, 6, 2, 17),
    task=1, location=1))

""" ZATERDAG """

shift_list.append(Shift(
    start=datetime(2023, 6, 3, 9),
    end=datetime(2023, 6, 3, 13),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 3, 13),
    end=datetime(2023, 6, 3, 18),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 3, 11),
    end=datetime(2023, 6, 3, 13),
    task=1, location=1))


""" ZONDAG """

shift_list.append(Shift(
    start=datetime(2023, 6, 4, 9),
    end=datetime(2023, 6, 4, 13),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 4, 13),
    end=datetime(2023, 6, 4, 18),
    task=1, location=1))

shift_list.append(Shift(
    start=datetime(2023, 6, 4, 11),
    end=datetime(2023, 6, 4, 13),
    task=1, location=1))

for id_, employee in enumerate(employee_list):
    employee.id = id_

for id_, shift in enumerate(shift_list):
    shift.id = id_
