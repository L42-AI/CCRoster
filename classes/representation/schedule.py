from classes.representation.workload import Workload

from data.assign import shift_list

class Schedule(dict):
    def __init__(self, Workload: Workload, cost: float, set_schedule: dict[int, int]):
        self.Workload = Workload
        self.cost = cost

        self.fitness: float = None
        self.p: float = None
        self.BUDS = 10 # number of buds this plant can have

        if set_schedule is not None:
            for shift_id in set_schedule:
                self[shift_id] = set_schedule[shift_id]

        else:
            for shift in shift_list:
                self[shift.id] = None