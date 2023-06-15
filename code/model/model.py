from tqdm import tqdm

from model.data.assign_mock import employee_list, shift_list

from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

from model.manipulate.fill import Fill, Greedy
from model.manipulate.PPA import PPA

from helpers import recursive_copy, gen_id_dict, gen_time_conflict_dict, gen_total_availabilities

class Model:

    """ DATABASE """

    def get_offline_data() -> tuple[list[Shift], list[Employee]]:
        return shift_list, employee_list
    
    def download(location_id: int) -> tuple[list[Shift], list[Employee]]:
        raise NotImplementedError
    
    """ SCHEDULE """

    def random(employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:
        return Model._random(employee_list, shift_list)

    def greedy(employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:
        return Model._greedy(employee_list, shift_list)

    def propagate(employee_list: list[Employee], shift_list: list[Shift], config: dict[str, str]) -> Schedule:
        schedule = Model._random(employee_list, shift_list)
        # schedule = Model._greedy(employee_list, shift_list)
        P = PPA(schedule)
        return P.grow(config)

    def optimal(employee_list: list[Employee], shift_list: list[Shift], config: dict[str, str]) -> Schedule:
        fail = 0
        schedule = None
        for _ in tqdm(range(int(config['optimize_runs']))):
            schedule = Model._greedy(employee_list, shift_list)
            if any(schedule.values()) == None:
                fail += 1
    
        fail_propotion = fail / 500
        print(fail_propotion)

        if schedule != None:
            return schedule
        return None

    """ GENERATORS """

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
