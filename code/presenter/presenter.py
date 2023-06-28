from tqdm import tqdm
from pprint import pprint
from model.model import Model
from view.view import View
from model.data.database import download

from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.shift import Shift
from model.representation.data_classes.employee import Employee

from helpers import gen_id_dict, recursive_copy, gen_total_availabilities

class Presenter:

    def __init__(self, config: dict[str, str]) -> None:
        self.config = config
        self.shift_list, self.employee_list = self._retrieve_data(self.config)

    def get_multi_schedules(self) -> list[Schedule]:
        if 'num_schedules' not in self.config:
            raise NameError(f'num_schedules missing from config file')
        
        iterations = int(self.config['num_schedules'])
        batches = int(iterations / 10)

        self.config['weights'] = recursive_copy(gen_total_availabilities(self.employee_list, self.shift_list))

        schedules = []
        print(f'Running {iterations} iterations in 10 batches')
        for _ in tqdm(range(10)):
            schedules_batch = []
            for _ in range(batches):
                schedule = self._build_schedule(self.config)

                schedules_batch.append(schedule)
                schedules.append(schedule)

            valid_schedules, invalid_schedules, shift_count_dict = Model.split_schedules(schedules_batch)
            valid_counts = Model.count_occupation(valid_schedules, recursive_copy(shift_count_dict))
            invalid_counts = Model.count_occupation(invalid_schedules, recursive_copy(shift_count_dict))
            Model.compute_weights(valid_counts, invalid_counts, self.config['weights'])
        return schedules

    def get_schedule(self) -> Schedule:
        return self._build_schedule(self.config)
    
    def graph_schedules(self, schedules: list[Schedule]):
        valid_schedules, invalid_schedules, shift_count_dict = Model.split_schedules(schedules)
        View.print_success_rate(invalid_schedules, valid_schedules)

        invalid_counts = Model.count_occupation(invalid_schedules, recursive_copy(shift_count_dict))
        valid_counts = Model.count_occupation(valid_schedules, recursive_copy(shift_count_dict))
        View.plot_schedules(valid_counts, invalid_counts, ['red', 'green'])

    def print_schedule(self, schedule: Schedule | None) -> None:
        if schedule != None:
            View.print_schedule(schedule, gen_id_dict(self.employee_list), gen_id_dict(self.shift_list))
        else:
            raise ValueError('No Schedule!')

    def _retrieve_data(self, config: dict[str, str]) -> tuple[list[Shift], list[Employee]]:
        match config['datatype']:
            case 'offline':
                return Model.get_offline_data()
            case 'online':
                return download(int(config['session_id']))
            case other:
                raise ValueError(f"{config['datatype']} not valid! Choose from:\n-'offline'\n-'online'")

    def _build_schedule(self, config: dict[str, str]) -> Schedule:
        match config['runtype']:
            case 'random':
                return Model.random(self.employee_list, self.shift_list)
            case 'greedy':
                return Model.greedy(self.employee_list, self.shift_list, self.config['weights'])
            case 'propagate':
                return Model.propagate(self.employee_list, self.shift_list, config)
            case 'optimal':
                return Model.optimal(self.employee_list, self.shift_list, config)
            case other:
                raise ValueError(f"{config['runtype']} not valid! Choose from:\n-'greedy'\n-'random'\n-'propagate'\n-'optimal'")
