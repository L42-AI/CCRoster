from tqdm import tqdm

from model.data.assign import employee_list, shift_list

from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

from model.manipulate.fill import Fill, Greedy
from model.manipulate.PPA import PPA

from helpers import recursive_copy, gen_id_dict, gen_time_conflict_dict, gen_total_availabilities

class Model:

    """ DATABASE """

    def get_offline_data():
        return shift_list, employee_list
    
    def download(location_id):
        ...
    
    """ SCHEDULE """

    def gen_random_schedule(employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:
        return Model._random(employee_list, shift_list)

    def gen_greedy_schedule(employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:
        return Model._greedy(employee_list, shift_list)

    def propagate(employee_list: list[Employee], shift_list: list[Shift], **kwargs) -> Schedule:
        schedule = Model._random(employee_list, shift_list)
        # schedule = Model._greedy(employee_list, shift_list)
        P = PPA(schedule, int(kwargs['num_plants']), int(kwargs['num_gens']))
        return P.grow(float(kwargs['temperature']))

    def optimal(employee_list: list[Employee], shift_list: list[Shift], **kwargs) -> Schedule:
        fail = 0
        for _ in tqdm(range(int(kwargs['optimize_runs']))):
            try:
                schedule = Model._greedy(employee_list, shift_list)
            except:
                fail += 1
        
        fail_propotion = fail / 500
        print(fail_propotion)

        if schedule != None:
            return schedule
        return None


    def _greedy(employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:
        G = Greedy(
            total_availabilities=recursive_copy(gen_total_availabilities(employee_list, shift_list)),
            time_conflict_dict=gen_time_conflict_dict(shift_list),
            id_employee=gen_id_dict(employee_list),
            id_shift=gen_id_dict(shift_list)
            )
        
        return G.generate(employee_list, shift_list)
    
    def _random(employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:
        F = Fill(
            total_availabilities=recursive_copy(gen_total_availabilities(employee_list, shift_list)),
            time_conflict_dict=gen_time_conflict_dict(shift_list),
            id_employee=gen_id_dict(employee_list),
            id_shift=gen_id_dict(shift_list)
            )
        
        return F.generate(employee_list, shift_list)
