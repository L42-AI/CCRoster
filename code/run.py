from model.manipulate.PPA import PPA
from model.data.assign import shift_list

import cProfile
import pstats
from io import StringIO

def run(PROFILE):
    if PROFILE:
        pr = cProfile.Profile()
        pr.enable()

        PPA(NUMBER_OF_PLANTS, NUMBER_OF_GENS, shift_list)
        
        pr.disable()

        # Create a StringIO object to store the profiling results
        s = StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')

        # Print the results, sorted by cumulative time
        ps.print_stats()
        print(s.getvalue())
    else:
        PPA(NUMBER_OF_PLANTS, NUMBER_OF_GENS, shift_list)


if __name__ == "__main__":
    NUMBER_OF_PLANTS = 300
    NUMBER_OF_GENS = 20
    PROFILE = False
    run(PROFILE)