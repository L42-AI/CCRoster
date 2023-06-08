from presenter.presenter import Presenter

config = {
    'datatype' : 'assign',
    'session_id' : 1,
    'runtype' : 'greedy',
    'num_plants' : '100',
    'num_gens' : '5',
    'temperature' : '0.5',
}

def main(config):
    P = Presenter(config)
    schedule = P.get_schedule()
    P.print_schedule(schedule)

if __name__ == "__main__":
    main(config)