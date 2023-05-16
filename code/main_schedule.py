from presentor.presentor import Presentor, Scheduler
from model.model import Model, Generator
from view.view import View, Viewer
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg

import matplotlib.pyplot as plt

session_id = 1
config = {
    'runtype' : 'propagate',
    'num_plants' : '200',
    'num_gens' : '40',
    'temperature' : '0.5',
}
config_dev = {
    'runtype' : 'propagate',
    'num_plants' : '100',
    'num_gens' : '5',
    'temperature' : '0.5',
}

import cProfile
import pstats
from io import StringIO

def run_scheduler(session_id, dev=False):
    score_adjust = []
    score_normal = []
    if dev:
        S = Scheduler(Generator, View, session_id)
        print(S.get_schedule(config_dev))
    else:
        S = Scheduler(Generator, View, session_id)
        for i in range(5):
            schedule = S.get_schedule(True, config)
            score_adjust.append(schedule.cost)
            print('done')
        for i in range(5):
            schedule = S.get_schedule(False, config)
            score_normal.append(schedule.cost)
            print('done')
        print(score_adjust)
        plt.hist(score_adjust, alpha=0.5, legend='adjust mutations', bins=10)
        plt.hist(score_normal, alpha=0.5, legend='do not adjust mutations', bins=10)
        plt.savefig('adjust_vs_not_adjust')
        plt.show()
        
if __name__ == "__main__":
    NUMBER_OF_PLANTS = 300
    NUMBER_OF_GENS = 20
    session_id = 1 # DEVELOPER DATA
    run_scheduler(session_id)