from classes.representation.generator import Generator
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

    
    # print(set(cost_list))
    plot(plot_dict, title='costs over 10000 iters')

""" PLOT """

def plot(plot_dict, title) -> None:
    plt.bar(plot_dict.keys(), plot_dict.values())
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    run()
    # Generator()