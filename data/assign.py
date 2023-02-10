from classes.representation.employee import Employee
import random


def cra() -> list:
    av = [0,0,0]
    av[0] = random.randint(0,2)
    av[1] = random.randint(0,6)
    av[2] = random.randint(0,1)
    return av


global employee_list
employee_list = []

employee_list.append(Employee('A. Becker', [cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra()], True))
employee_list.append(Employee('B. Becker', [cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra()], True))
employee_list.append(Employee('C. Becker', [cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra()], True))
employee_list.append(Employee('D. Becker', [cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra()], True))
employee_list.append(Employee('E. Becker', [cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra()], True))
employee_list.append(Employee('F. Becker', [cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra(),cra()], True))
