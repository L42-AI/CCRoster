from typing import Protocol
from model.data.manipulate import PPA

class Model(Protocol):
    def upload_assign(shift_list, employee_list):
        ...
    
    def propagate():
        PPA = PPA()