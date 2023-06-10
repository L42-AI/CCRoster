from model.model import Model
from view.view import View
from model.data.database import download

from helpers import gen_id_dict

class Presenter:

    def __init__(self, config) -> None:
        self.config = config
        self.shift_list, self.employee_list = self._retrieve_data(self.config)

    def get_schedule(self):
        return self._build_schedule(self.config)
    
    def print_schedule(self, schedule):
        View.print_schedule(schedule, gen_id_dict(self.employee_list), gen_id_dict(self.shift_list))

    def _retrieve_data(self, config):
        match config['datatype']:
            case 'offline':
                return Model.get_offline_data()
            case 'online':
                return download(int(config['session_id']))
            case other:
                raise ValueError(f"{config['datatype']} not valid! Choose from: 'offline' or 'online'")

    def _build_schedule(self, config):
        match config['runtype']:
            case 'random':
                return Model.gen_random_schedule(self.employee_list, self.shift_list)
            case 'greedy':
                return Model.gen_greedy_schedule(self.employee_list, self.shift_list)
            case 'propagate':
                return Model.propagate(self.employee_list, self.shift_list, **config)
            case 'optimal':
                return Model.optimal(self.employee_list, self.shift_list, **config)
            case other:
                raise ValueError(f"{config['runtype']} not valid! Choose from: 'greedy', 'random' or 'propagate'")
