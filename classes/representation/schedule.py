class Schedule():
    def __init__(self, workload, init_schedule, cost):
        self.workload = workload
        self.schedule = init_schedule
        self.cost = cost
        self.fitness: float = None
        self.p: float = None
        self.BUDS = 10 # number of buds this plant can have
    
