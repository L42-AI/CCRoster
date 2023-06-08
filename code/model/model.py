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

class Model():
    """ DATABASE """
    def upload(shift_list, employee_list):
        ...
    
    def download(location_id):
        ...
    
    """ SCHEDULE """

    def create_random_schedule(**config):
        return Fill.fill(AbsSchedule(Workload(config['shifts'], config['employees'])))

    def create_greedy_schedule(**config):
        return Greedy.fill(config['employees'], config['shifts'], Schedule(Workload(config['shifts'], config['employees']), CurrentAvailabilities()))

    def propagate(**config):

        # create a shift constraints instance that will be used by PPA and Fill
        shift_constraints = Shiftconstraints(config['shifts'], config['employees'])
        config['shiftconstraints'] = shift_constraints

        # create Fill
        FillClass = Fill(shift_constraints)
        schedule = FillClass.fill(AbsSchedule(Workload(config['shifts'], config['employees'])))

        P = PPA(schedule, **config)
        schedule = P.grow()

        return schedule

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
    

