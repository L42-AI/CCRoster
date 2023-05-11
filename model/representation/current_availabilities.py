
from data.schedule_constants import total_availabilities

class CurrentAvailabilities(dict):
    def __init__(self):

        for shift_id, shift_availability in total_availabilities.items():
            self[shift_id] = [0, shift_availability]