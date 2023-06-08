from presenter.presenter import Presenter

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