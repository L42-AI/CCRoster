from model.representation.data_classes.employee import Employee, Availability
from model.representation.data_classes.shift import Shift

from model.data.database import download
from model.model import Model

class Presenter:
    ''' Handles traffic between Viewer and Model. Now always downloads employees and shifts
        when initialised, that should perheaps be changed in a later stage (let the methods receive
        a session_id so they can download themself?)'''
    def __init__(self, session_id: int) -> None:
        self.shift_list, self.employee_list = download(session_id)

    def get_schedule(self, config):
        config['employees'] = self.employee_list
        config['shifts'] = self.shift_list
        
        if config['runtype'] == 'random':
            schedule = Model.create_random_schedule(**config)
        elif config['runtype'] == 'greedy':
            schedule = Model.create_greedy_schedule(**config)
        elif config['runtype'] == 'propagate':
            schedule = Model.propagate(**config)
        else:
            raise ValueError(f"{config['runtype']} not valid! Choose from: 'greedy', 'random' or 'propagate'")
        
        return schedule
    
    def display_schedule():
        ...

    def get_employees(self):
        return self.employee_list

    def display_employees():
        ...    

    def get_shifts(self):
        return self.shift_list

    def display_shifts():
        ...
    

    
   