from typing import Protocol

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