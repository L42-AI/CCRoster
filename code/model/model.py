from typing import Protocol

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

    def create_random_schedule(self,):
        pass

    def propagate(self,num_plants, num_gens, shift_list, temperature):
        pass