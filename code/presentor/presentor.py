from typing import Protocol
import random
from model.model import Model, Generator
from model.representation.data_classes.employee import Employee, Availability
from model.representation.data_classes.shift import Shift

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
        self.shift_list, self.employee_list = download(session_id)


    def get_schedule(self, adjust_, config):
        config['employees'] = self.employee_list
        config['shifts'] = self.shift_list
        if config['runtype'] == 'random':
            schedule = Generator.create_random_schedule()
        elif config['runtype'] == 'greedy':
            schedule = Generator.create_greedy_schedule(self.employee_list, self.shift_list)
        elif config['runtype'] == 'propagate':
            schedule = Generator.propagate(self.employee_list, self.shift_list, adjust=adjust_, **config)
        else:
            raise ValueError(f"{config['runtype']} not valid! Choose from: 'greedy', 'random' or 'propagate'")
        
        return schedule
    
    
    

    
   