from classes.representation.budding import Generator
import cProfile
import pstats
from io import StringIO
import matplotlib.pyplot as plt
from tqdm import tqdm

""" TEST """


def run() -> None:
    plot_dict = {}
    for i in tqdm(range(10000)):
        G = Generator()
        cost = str(G.total_costs)
        if cost not in plot_dict:
            plot_dict[cost] = 1
        else:
            plot_dict[cost] += 1
    print(plot_dict)
    plt.plot(plot_dict, title='costs over 10000 iters')

""" PLOT """

def plot(plot_dict: dict[int, int], title: str) -> None:
    plt.bar(plot_dict.keys(), plot_dict.values())
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    # run()
    pr = cProfile.Profile()
    pr.enable()
    Generator()
    
    pr.disable()

    # Create a StringIO object to store the profiling results
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')

    # Print the results, sorted by cumulative time
    ps.print_stats()
    print(s.getvalue())