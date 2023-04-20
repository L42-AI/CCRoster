import random

from classes.representation.generator import Generator
from classes.representation.workload import Workload
from classes.representation.plant import Plant

from helpers import recursive_copy
from data.assign import employee_list, shift_list, total_availabilities

class PlantPropagation:
    def __init__(self, num_plants: int, num_gens: int) -> None:
        self.gen = Generator()
        self.gen.greedy_fill()

        self.NUMBER_OF_PLANTS = num_plants
        self.NUMBER_OF_GENERATIONS = num_gens

        self.plants(self.gen, self.NUMBER_OF_PLANTS, self.NUMBER_OF_GENERATIONS)


    def plants(self, gen: Generator, NUMBER_OF_PLANTS: int, NUMBER_OF_GENERATIONS: int):
        forest = []
        forest_costs = []
        for plant in range(NUMBER_OF_PLANTS):
            # start with a sim an probability of 0
            new_plant = Plant(0, recursive_copy(gen.schedule), Workload(recursive_copy(gen.Workload)))
            forest.append(new_plant)

        for generation in range(NUMBER_OF_GENERATIONS):
            forest = sorted(forest, key= lambda x: x.total_costs)
            for plant in forest:
                print(plant.total_costs)
            print('--------------------------------')
            forest_costs = []
            for index, plant in enumerate(forest):
                plant.sim_an = index / (NUMBER_OF_PLANTS * 1000 ) if index > 20 else 0
                plant.improve(200)
        
        winner = min(forest, key= lambda x: x.total_costs)
        return winner.schedule