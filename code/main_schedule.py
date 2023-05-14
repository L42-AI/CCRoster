from presentor.presentor import Presentor, Scheduler
from model.model import Model, Generator
from view.view import View, Viewer

from model.data.assign import shift_list, employee_list

config = {
    'runtype' : 'propagate',
    'num_plants' : '300',
    'num_gens' : '20',
    'temperature' : '0.5',
}

import cProfile
import pstats
from io import StringIO

def run_scheduler(session_id):

    S = Scheduler(Generator, View, session_id)
    print(S.get_schedule(config))


if __name__ == "__main__":
    NUMBER_OF_PLANTS = 300
    NUMBER_OF_GENS = 20
    session_id = 1 # DEVELOPER DATA
    run_scheduler(session_id)