from model.model import Model
from view import View

from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.shift import Shift
from model.representation.data_classes.employee import Employee
from model.data.database import download

from helpers import gen_id_dict, recursive_copy

class Presenter:

    def __init__(self, config: dict[str, str]) -> None:
        self.config = config
        self.shift_list, self.employee_list = self._retrieve_data(self.config)

    def get_schedule(self) -> Schedule:
        return self._build_schedule(self.config)
    
    def get_schedules(self) -> Schedule:
        if self.config['runtype'] not in ['multi']:
            raise ValueError(f"{self.config['datatype']} not valid! Choose from:\n-'multi'")
        return Model.multi_schedules(self.employee_list, self.shift_list, self.config)
    
    def graph_schedules(self, schedules: list[Schedule]):
        if not isinstance(schedules, list):
            raise IndexError('Schedules are not a list')
        
        valid_schedules, invalid_schedules, shift_count_dict = Model.split_schedules(schedules)
        View.print_success_rate(valid_schedules, invalid_schedules)

        valid_counts = Model.count_occupation(valid_schedules, recursive_copy(shift_count_dict))
        invalid_counts = Model.count_occupation(invalid_schedules, recursive_copy(shift_count_dict))
        View.plot_schedules(valid_counts, invalid_counts, ['red', 'green'])

    def print_schedule(self, schedule: Schedule | None) -> None:
        if schedule is None:
            raise ValueError('No Schedule!')
        
        View.print_schedule(schedule, gen_id_dict(self.employee_list), gen_id_dict(self.shift_list))

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
                return Model.greedy(self.employee_list, self.shift_list)
            case 'propagate':
                return Model.propagate(self.employee_list, self.shift_list, config)
            case 'optimal':
                return Model.optimal(self.employee_list, self.shift_list, config)
            case other:
                raise ValueError(f"{config['runtype']} not valid! Choose from:\n-'greedy'\n-'random'\n-'propagate'\n-'optimal'")
