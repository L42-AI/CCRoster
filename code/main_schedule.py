from presenter.presenter import Presenter
from model.model import Model, Generator
from view.view import View, Viewer
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg

import matplotlib.pyplot as plt
import csv
session_id = 1
configurations = [
    # {
    #     'runtype': 'propagate',
    #     'num_plants': '100',
    #     'num_gens': '60',
    #     'temperature': '0.5',
    # },
    #  {
    #     'runtype': 'propagate',
    #     'num_plants': '100',
    #     'num_gens': '40',
    #     'temperature': '0.5',
    # },
    #  {
    #     'runtype': 'propagate',
    #     'num_plants': '100',
    #     'num_gens': '30',
    #     'temperature': '0.5',
    # },
    # {
    #     'runtype': 'propagate',
    #     'num_plants': '200',
    #     'num_gens': '60',
    #     'temperature': '0.5',
    # },
    # {
    #     'runtype': 'propagate',
    #     'num_plants': '200',
    #     'num_gens': '40',
    #     'temperature': '0.5',
    # },
    # {
    #     'runtype': 'propagate',
    #     'num_plants': '200',
    #     'num_gens': '60',
    #     'temperature': '0.9',
    # } ''' '''
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
    'runtype' : 'propagate',
    'num_plants' : '100',
    'num_gens' : '5',
    'temperature' : '0.5',
}

import cProfile
import pstats
from io import StringIO

def plot_results(session_id, dev=False):
    presenter = Presenter(Generator, session_id)
    fig, ax = plt.subplots()

    data = []
    for i, config in enumerate(configurations):
        scores = []
        for _ in range(30):
            print(f'i: {i}, #: {_}')
            schedule = presenter.get_schedule(config)
            scores.append(schedule.cost)
        
        ax.hist(scores, alpha=0.4, label=f'PPA config{i+7}', bins=10)
        data.extend([(f'PPA config{i+7}', score) for score in scores])

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xlabel('Cost')
    plt.ylabel('Frequency')
    plt.title('PPA Results')
    plt.savefig('PPA_results.png')
    plt.show()

    # Store data in a CSV file
    output_file = 'PPA_results.csv'
    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Configuration', 'Cost'])
        writer.writerows(data)

    print(f'Data exported to {output_file}.')
        
def run_once(session_id, dev=False):
    if dev:
        presenter= Presenter(Generator, session_id)
        print(presenter.get_schedule(config_dev))
    else:
        presenter= Presenter(Generator, session_id)
        print(presenter.get_schedule(config))

if __name__ == "__main__":
    NUMBER_OF_PLANTS = 300
    NUMBER_OF_GENS = 20
    session_id = 1 # DEVELOPER DATA
    plot_results(session_id)