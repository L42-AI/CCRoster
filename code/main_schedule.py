from presenter.presenter import Presenter

config = {
    'datatype' : 'offline',
    'session_id' : '1',
    'runtype' : 'multi',
    'num_plants' : '100',
    'num_gens' : '5',
    'temperature' : '0.5',
    'optimize_runs' : '2000',
    'num_schedules' : '100000'
}

def main(config):
    P = Presenter(config)
    # schedule = P.get_schedule()
    schedules = P.get_schedules()
    P.graph_schedules(schedules)
    # P.print_schedule(schedule)

if __name__ == "__main__":
    main(config)