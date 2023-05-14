from typing import Protocol
from model.model import Model, Generator
from view.view import View

class Presentor(Protocol):
    def get_schedule():
        ...
    
    def display_schedule():
        ...

    def get_shifts():
        ...
    
    def display_shifts():
        ...

    def get_employees():
        ...
    
    def display_employees():
        ...

class Scheduler(Presentor):

    def __init__(self, Model: Model, View: View) -> None:
        self.Model = Model
        self.View = View

    def get_schedule(self, employee_list, shift_list, config):
        if config['runtype'] == 'random':
            schedule = Generator.create_random_schedule()
        elif config['runtype'] == 'greedy':
            schedule = Generator.create_greedy_schedule(employee_list, shift_list)
        elif config['runtype'] == 'propagate':
            schedule = Generator.propagate(employee_list, shift_list, **config)
        else:
            raise ValueError(f"{config['runtype']} not valid! Choose from: 'greedy', 'random' or 'propagate'")
        
        return schedule
