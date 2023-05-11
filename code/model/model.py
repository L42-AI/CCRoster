from typing import Protocol

from model.representation.data_classes.schedule import AbsSchedule, Schedule
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift
from model.representation.data_classes.current_availabilities import CurrentAvailabilities

from model.manipulate.fill import Fill, Greedy
from model.manipulate.PPA import PPA

class Model(Protocol):
    """ DATABASE """
    def upload(shift_list, employee_list):
        ...
    
    def download(location_id):
        ...
    
    """ SCHEDULE """
    def create_random_schedule():
        ...

    def create_greedy_schedule(employee_list: list[Employee], shift_list: list[Shift]):
        ...

    def propagate(shift_list, **kwargs):
        ...

class DB(Model):
    def upload(self, shift_list, employee_list):
        pass
    
    def download(self, location_id):
        pass

class Generator(Model):

    def create_random_schedule():
        return Fill.fill(AbsSchedule(Workload()))

    def create_greedy_schedule(employee_list: list[Employee], shift_list: list[Shift]):
        return Greedy.fill(employee_list, shift_list, Schedule(Workload(), CurrentAvailabilities()))

    def propagate(shift_list, **kwargs):
        schedule = Fill.fill(AbsSchedule(Workload()))
        P = PPA(schedule, int(kwargs['num_plants']), int(kwargs['num_gens']))
        P.grow(float(kwargs['temperature']))
