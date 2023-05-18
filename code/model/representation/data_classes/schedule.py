import random
import random
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from model.representation.data_classes.current_availabilities import CurrentAvailabilities
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.setup import Base


class AbsSchedule(dict):
    def __init__(self, Workload: Workload, set_schedule: dict[int, int] = None):
        self.Workload = Workload
        if set_schedule is not None:
            for shift_id in set_schedule:
                self[shift_id] = set_schedule[shift_id]
        else:
            for shift in self.Workload.shift_list:
                self[shift.id] = None

class Schedule(AbsSchedule):
    def __init__(self, Workload: Workload, CurrentAvailabilities: CurrentAvailabilities, set_schedule: dict[int, int] = None):
        super().__init__(Workload, set_schedule)
        self.CurrentAvailabilities = CurrentAvailabilities

class Plant(AbsSchedule):
    def __init__(self, Workload: Workload, cost: float, set_schedule: dict[int, int] = None):
        super().__init__(Workload, set_schedule)

        self.cost = cost
        self.fitness: float = None
        self.p: float = None
        self.BUDS = 10 # number of buds this plant can have
        self.MUTATIONS = random.randint(3, 20)

class UploadSchedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.now())
    def __init__(self, workload_dict: dict[int, list[int]], schedule_dict: dict[int, int]):
        self.workload = workload_dict
        self.schedule = schedule_dict
