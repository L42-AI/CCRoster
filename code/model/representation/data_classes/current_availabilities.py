from pprint import pprint

class CurrentAvailabilities(dict):
    def __init__(self, total_availabilities: dict[int, dict[int, int]]):
        self.total_availabilities = total_availabilities

        for shift_id, shift_availability in total_availabilities.items():
            start_proportion = 1 / len(shift_availability)
            self[shift_id] = [0, {employee_id: start_proportion for employee_id in shift_availability}]