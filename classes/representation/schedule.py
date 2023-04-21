from classes.representation.workload import Workload

class Schedule():
    def __init__(self, Workload: Workload, init_schedule, cost):
        self.Workload = Workload
        self.schedule = init_schedule
        self.cost = cost
        self.fitness: float = None
        self.p: float = None
        self.BUDS = 10 # number of buds this plant can have
    
