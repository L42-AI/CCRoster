from classes.representation.generator import Generator
import matplotlib.pyplot as plt
from tqdm import tqdm

""" TEST """

def run() -> None:
    iter_list = []
    cost_list = []
    for i in tqdm(range(10000)):
        G = Generator()
        cost = G.total_costs

        iter_list.append(i)
        cost_list.append(cost)
    
    print(set(cost_list))
    plot(cost_list, iter_list, title='costs over 10000 iters')

""" PLOT """

def plot(x_list:list, y_list:list, title: str) -> None:
    plt.bar(x_list, y_list)
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    # run()
    Generator()