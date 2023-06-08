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
    def get_standard_cost(employee_list: list[Employee]) -> float:
        total = sum([employee.get_minimal_hours() * employee.get_wage()  for employee in employee_list])

        return round(total, 2)
    
    def get_total_availabilties(employee_list: list[Employee], shift_list: list[Shift]) -> dict:
        return {shift.id: Shiftconstraints.get_employee_set(shift, employee_list) for shift in shift_list}

    def get_coliding_dict(shifts_list: list[Shift]) -> dict[int, set[int]]:

        time_conflict_dict = {shift.id: set() for shift in shifts_list}

        for i, shift_1 in enumerate(shifts_list):

            for shift_2 in shifts_list[i+1:]:
                if shift_1.end < shift_2.start:
                    continue
                if shift_1.start < shift_2.end:
                    time_conflict_dict[shift_1.id].add(shift_2.id)
                    time_conflict_dict[shift_2.id].add(shift_1.id)

        return time_conflict_dict

    def create_random_schedule(**config) -> AbsSchedule:
        Filler = Fill(Shiftconstraints(config['shifts'], config['employees']))
        return Filler.fill(AbsSchedule(Workload(config['shifts'], config['employees'])))

    def create_greedy_schedule(**config) -> AbsSchedule:
        Filler = Greedy(Shiftconstraints(config['shifts'], config['employees']))
        return Filler.fill(config['employees'], config['shifts'], Schedule(Workload(config['shifts'], config['employees']), CurrentAvailabilities(config['total_availabilities'])))

    def propagate(**config) -> AbsSchedule:
        # create a shift constraints instance that will be used by PPA and Fill
        shift_constraints = Shiftconstraints(config['shifts'], config['employees'])
        config['shiftconstraints'] = shift_constraints

        # create Fill
        FillClass = Fill(shift_constraints)
        schedule = FillClass.fill(AbsSchedule(Workload(config['shifts'], config['employees'])))

        P = PPA(schedule, **config)
        schedule = P.grow()

        return schedule

