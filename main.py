from improve.PPA import PPA

import cProfile
import pstats
from io import StringIO

def main(PROFILE):

    

    if PROFILE:
        pr = cProfile.Profile()
        pr.enable()

        PPA(NUMBER_OF_PLANTS, NUMBER_OF_GENS)
        
        pr.disable()

        # Create a StringIO object to store the profiling results
        s = StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')

        # Print the results, sorted by cumulative time
        ps.print_stats()
        print(s.getvalue())
    else:
        PPA(NUMBER_OF_PLANTS, NUMBER_OF_GENS)


if __name__ == "__main__":
    NUMBER_OF_PLANTS = 300
    NUMBER_OF_GENS = 20
    PROFILE = False
    main(PROFILE)