from presenter.presenter import Presenter

config = {
    'datatype' : 'offline',
    'session_id' : '1',
    'runtype' : 'propagate',
    'num_plants' : '100',
    'num_gens' : '5',
    'temperature' : '0.5',
    'optimize_runs' : '500'
}

def main(config):
    P = Presenter(config)
    schedule = P.get_schedule()
    print(schedule)
    P.print_schedule(schedule)

if __name__ == "__main__":
    main(config)