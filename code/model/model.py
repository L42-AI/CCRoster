from tqdm import tqdm

from model.data.assign_mock import employee_list, shift_list

from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

from model.manipulate.fill import Fill, Greedy
from model.manipulate.PPA import PPA

from helpers import recursive_copy, gen_id_dict, gen_time_conflict_dict, gen_total_availabilities, softmax_function, improved_softmax_function

class Model:

    """ DATABASE """

    def get_offline_data() -> tuple[list[Shift], list[Employee]]:
        return shift_list, employee_list
    
    def download(location_id: int) -> tuple[list[Shift], list[Employee]]:
        raise NotImplementedError
    
    """ SCHEDULE """

    def random(employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:
        return Model._random(employee_list, shift_list)

    def greedy(employee_list: list[Employee], shift_list: list[Shift], weights: dict[int, dict[int, int]] = None) -> Schedule:
        return Model._greedy(employee_list, shift_list, weights)

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

    def multi_schedules(employee_list: list[Employee], shift_list: list[Shift], config: dict[str, str]) -> list[Schedule]:
        if 'num_schedules' not in config:
            raise NameError(f'num_schedules missing from config file')
        
        iterations = int(config['num_schedules'])
        weights = recursive_copy(gen_total_availabilities(employee_list, shift_list))

        schedules = []
        print(f'Running {iterations} iterations in 10 batches')
        for _ in tqdm(range(10)):
            schedules_batch = []
            for _ in range(int(iterations / 10)):
                schedule = Model._greedy(employee_list, shift_list, weights)

                schedules_batch.append(schedule)
                schedules.append(schedule)

            weights = Model.compute_weights(schedules_batch, recursive_copy(weights))
        return schedules

    """ GENERATORS """

    def _greedy(employee_list: list[Employee], shift_list: list[Shift], weights: dict[int, dict[int, int]] = None) -> Schedule:
        G = Greedy(
            total_availabilities=recursive_copy(gen_total_availabilities(employee_list, shift_list)),
            time_conflict_dict=gen_time_conflict_dict(shift_list),
            id_employee=gen_id_dict(employee_list),
            id_shift=gen_id_dict(shift_list)
            )
        
        return G.generate(employee_list, shift_list, weights)
    
    def _random(employee_list: list[Employee], shift_list: list[Shift]) -> Schedule:
        F = Fill(
            total_availabilities=recursive_copy(gen_total_availabilities(employee_list, shift_list)),
            time_conflict_dict=gen_time_conflict_dict(shift_list),
            id_employee=gen_id_dict(employee_list),
            id_shift=gen_id_dict(shift_list)
            )
        
        return F.generate(employee_list, shift_list)

    """ SCHEDULES PROCESSING """

    def split_schedules(schedules: list[Schedule]) -> tuple[list[Schedule], list[Schedule]]:

        shift_count_dict = {shift_id: {} for shift_id in schedules[0]}

        valid_schedules = []
        invalid_schedules = []

        for schedule in schedules:

            for shift_id, employee_id in schedule.items():
                if employee_id not in shift_count_dict[shift_id]:
                    shift_count_dict[shift_id][str(employee_id)] = 0

            if Model._has_none_values(schedule):
                invalid_schedules.append(schedule)
            else:
                valid_schedules.append(schedule)
        
        return valid_schedules, invalid_schedules, shift_count_dict

    def count_occupation(schedules: list[Schedule], shift_count_dict: dict[int, dict[int, int]]) -> dict[int, dict[int, int]]:
        for schedule in schedules:
            for shift_id, employee_id in schedule.items():
                shift_count_dict[shift_id][str(employee_id)] += 1

        return shift_count_dict
    
    @staticmethod
    def compute_weights(schedules: list[Schedule], weights):
        valid_schedules, invalid_schedules, shift_count_dict = Model.split_schedules(schedules)
        valid_counts = Model.count_occupation(valid_schedules, recursive_copy(shift_count_dict))
        invalid_counts = Model.count_occupation(invalid_schedules, recursive_copy(shift_count_dict))
        
        validity_rate = len(valid_schedules) / len(invalid_schedules)
        for shift in valid_counts:
            for employee in valid_counts[shift]:
                if employee == 'None':
                    continue
                employee_validity_rate = valid_counts[shift][employee] / (valid_counts[shift][employee] + invalid_counts[shift][employee])
                
                weights[shift][int(employee)] = employee_validity_rate / validity_rate
        
        for shift in weights:
            softmax_outputs = improved_softmax_function(list(weights[shift].values()))
            for i, employee in enumerate(weights[shift]):
                weights[shift][employee] = softmax_outputs[i]
        
        return weights




    def _has_none_values(data_dict: dict):
        for value in data_dict.values():
            if value is None:
                return True
        return False