from model.data.assign import employee_list, shift_list

from model.representation.data_classes.schedule import AbsSchedule, Schedule
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift
from model.representation.data_classes.current_availabilities import CurrentAvailabilities

from model.manipulate.fill import Fill, Greedy
from model.manipulate.PPA import PPA

class Model:
    """ DATABASE """
    def get_offline_data():
        return employee_list, shift_list
    
    def download(location_id):
        ...
    
    """ SCHEDULE """
    def create_random_schedule():
        return Fill.fill(AbsSchedule(Workload()))

    def create_greedy_schedule(employee_list: list[Employee], shift_list: list[Shift]):
        return Greedy.fill(employee_list, shift_list, Schedule(Workload(), CurrentAvailabilities()))

    def propagate(employee_list: list[Employee], shift_list: list[Shift], **kwargs):
        schedule = Fill.fill(AbsSchedule(Workload()))
        # schedule = Greedy.fill(employee_list, shift_list, Schedule(Workload(), CurrentAvailabilities()))
        P = PPA(schedule, int(kwargs['num_plants']), int(kwargs['num_gens']))
        P.grow(float(kwargs['temperature']))