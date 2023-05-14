from typing import Protocol
from model.model import Model, Generator
from view.view import View
from model.data.database import download

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

    def __init__(self, Model: Model, View: View, session_id: int) -> None:
        self.Model = Model
        self.View = View
        self.employee_list, self.shift_list = download(session_id)

    def get_schedule(self, config):
        if config['runtype'] == 'random':
            schedule = Generator.create_random_schedule()
        elif config['runtype'] == 'greedy':
            schedule = Generator.create_greedy_schedule(self.employee_list, self.shift_list)
        elif config['runtype'] == 'propagate':
            schedule = Generator.propagate(self.employee_list, self.shift_list, **config)
        else:
            raise ValueError(f"{config['runtype']} not valid! Choose from: 'greedy', 'random' or 'propagate'")
        
        return schedule
