from typing import Protocol

from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

from model.manipulate.fill import Greedy

class Model(Protocol):
    """ DATABASE """
    def upload(shift_list, employee_list):
        ...
    
    def download(location_id):
        ...
    
    """ SCHEDULE """
    def create_random_schedule():
        ...

    def create_greedy_schedule():
        ...

    def propagate(num_plants, num_gens, shift_list, temperature):
        ...

class DB(Model):
    def upload(self, shift_list, employee_list):
        pass
    
    def download(self, location_id):
        pass

class Generator(Model):

    def create_random_schedule(self,):
        pass

    def create_greedy_schedule(self, employee_list: list[Employee], shift_list: list[Shift]):
        return Greedy.greedy_fill(employee_list, shift_list, Schedule(Workload(), 99999))

    def propagate(self,num_plants, num_gens, shift_list, temperature):
        pass