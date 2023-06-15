from model.model import Model
from view.view import View
from model.data.database import download

from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.shift import Shift
from model.representation.data_classes.employee import Employee

from helpers import gen_id_dict

class Presenter:

    def __init__(self, config: dict[str, str]) -> None:
        self.config = config
        self.shift_list, self.employee_list = self._retrieve_data(self.config)

    def get_schedule(self) -> Schedule:
        return self._build_schedule(self.config)
    
    def print_schedule(self, schedule: Schedule | None) -> None:
        if schedule != None:
            View.print_schedule(schedule, gen_id_dict(self.employee_list), gen_id_dict(self.shift_list))
        else:
            print('No Schedule!')

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
