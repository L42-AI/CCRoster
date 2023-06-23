from presenter.presenter import Presenter
from model.model import Model, Generator
from view.view import View, Viewer
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg

import matplotlib.pyplot as plt
import csv
session_id = 1
configurations = [
    {
        'runtype': 'propagate',
        'num_plants': '100',
        'num_gens': '60',
        'temperature': '0.5',
    },
     {
        'runtype': 'propagate',
        'num_plants': '100',
        'num_gens': '100',
        'temperature': '0.9',
    },
    {
        'runtype': 'propagate',
        'num_plants': '100',
        'num_gens': '30',
        'temperature': '0.5',
    },
    {
        'runtype': 'propagate',
        'num_plants': '200',
        'num_gens': '60',
        'temperature': '0.5',
    },
    {
        'runtype': 'propagate',
        'num_plants': '200',
        'num_gens': '40',
        'temperature': '0.5',
    },
    {
        'runtype': 'propagate',
        'num_plants': '200',
        'num_gens': '60',
        'temperature': '0.9',
    }, 
    {
        'runtype': 'propagate',
        'num_plants': '300',
        'num_gens': '60',
        'temperature': '0.5',
    },
    {
        'runtype': 'propagate',
        'num_plants': '300',
        'num_gens': '40',
        'temperature': '0.5',
    },
    {
        'runtype': 'propagate',
        'num_plants': '300',
        'num_gens': '60',
        'temperature': '0.9',
    },
    {
        'runtype': 'propagate',
        'num_plants': '300',
        'num_gens': '30',
        'temperature': '0.5',
    },
    {
        'runtype': 'propagate',
        'num_plants': '400',
        'num_gens': '60',
        'temperature': '0.5',
    },
    {
        'runtype': 'propagate',
        'num_plants': '400',
        'num_gens': '40',
        'temperature': '0.5',
    }
#     # { # this one always gets stuck somehow..
#     #     'runtype': 'propagate',
#     #     'num_plants': '400',
#     #     'num_gens': '20',
#     #     'temperature': '0.5',
#     # }
]


config_dev = {
    'runtype' : 'greedy',
    'num_plants' : '100',
    'num_gens' : '5',
    'temperature' : '0.5',
}

def main(session_id):
    P = Presenter(session_id)
    print(P.get_schedule(config_dev))

if __name__ == "__main__":
    session_id = 1 # DEVELOPER DATA
    main(session_id)