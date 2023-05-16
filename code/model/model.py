from typing import Protocol

from model.representation.data_classes.schedule import AbsSchedule, Schedule
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.employee import Employee, Availability
from model.representation.data_classes.shift import Shift
from model.representation.data_classes.current_availabilities import CurrentAvailabilities
from model.representation.behaviour_classes.malus_calc import MalusCalc
from model.representation.behaviour_classes.shift_constraints import Shiftconstraints

from model.manipulate.fill import Fill, Greedy
from model.manipulate.PPA import PPA

class Model(Protocol):
    """ DATABASE """
    def upload(shift_list, employee_list):
        ...
    
    def download(location_id):
        ...
    
    """ SCHEDULE """
    def create_random_schedule():
        ...

    def create_greedy_schedule(employee_list: list[Employee], shift_list: list[Shift]):
        ...

    def propagate(shift_list, **kwargs):
        ...

class DB(Model):
    def upload(self, shift_list, employee_list):
        pass
    
    def download(self, user_id):
        pass

class Generator(Model):

    def create_random_schedule():
        return Fill.fill(AbsSchedule(Workload()))

    def create_greedy_schedule(employee_list: list[Employee], shift_list: list[Shift]):
        return Greedy.fill(employee_list, shift_list, Schedule(Workload(), CurrentAvailabilities()))

    def propagate(employee_list: list[Employee], shift_list: list[Shift], **kwargs):

        # create a shift constraints instance that will be used by PPA and Fill
        shift_constraints = Shiftconstraints(kwargs['shifts'], kwargs['employees'])
        kwargs['shiftconstraints'] = shift_constraints

        # create Fill
        FillClass = Fill(shift_constraints)
        schedule = FillClass.fill(AbsSchedule(Workload(shift_list, employee_list)))

        P = PPA(schedule, **kwargs)
        schedule = P.grow()

        return schedule
    

