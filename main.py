from classes.representation.generator import Generator
import matplotlib.pyplot as plt
from tqdm import tqdm

SINGLE = 1

""" TEST """

def run() -> None:
    plot_dict = {}
    for i in tqdm(range(1000)):
        G = Generator()
        cost = G.total_costs
        if cost not in plot_dict:
            plot_dict[cost] = 1
        else:
            plot_dict[cost] += 1
    print(plot_dict)
    plot_bar(plot_dict, title='costs over 10000 iters')

""" PLOT """

def plot_bar(plot_dict: dict[int, int], title: str) -> None:
    plt.bar(x=plot_dict.keys(), height=plot_dict.values())
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    if SINGLE:
        Generator()
    else:
        run()