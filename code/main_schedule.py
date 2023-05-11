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

def run(PROFILE):
    if PROFILE:
        pr = cProfile.Profile()
        pr.enable()

        S = Scheduler(Generator, View)
        S.get_schedule(employee_list, shift_list, config)
        
        pr.disable()

        # Create a StringIO object to store the profiling results
        s = StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')

        # Print the results, sorted by cumulative time
        ps.print_stats()
        print(s.getvalue())
    else:
        S = Scheduler(Generator, View)
        print(S.get_schedule(employee_list, shift_list, config))


if __name__ == "__main__":
    NUMBER_OF_PLANTS = 300
    NUMBER_OF_GENS = 20
    PROFILE = False
    run(PROFILE)