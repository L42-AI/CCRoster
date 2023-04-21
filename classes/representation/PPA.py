import random
import itertools

from classes.representation.generator import Generator
from classes.representation.workload import Workload
from classes.representation.schedule import Schedule

from helpers import recursive_copy, get_temperature
from data.assign import employee_list, shift_list, total_availabilities

class PlantPropagation:
    def __init__(self, num_plants: int, num_gens: int, TEMPERATURE=.5) -> None:
        self.gen: Generator = Generator()
        self.gen.greedy_fill()
        self.Schedule = self.gen.Schedule # not necessary but better readability imo
        self.NUMBER_OF_PLANTS: int = num_plants
        self.NUMBER_OF_GENERATIONS: int = num_gens
        self.T: int = TEMPERATURE

        self.plants()


    def plants(self):
        plants = [Schedule(self.Schedule.Workload, self.Schedule.cost, recursive_copy(self.Schedule)) for i in range(100)]
        for _ in range(2000):
            self.T = get_temperature(self.T)
            plants_and_buds = [self.gen.mutate(plant, self.T) for plant in plants]
            plants_and_buds = list(itertools.chain(*plants_and_buds))
            plants_and_buds = sorted(plants_and_buds, key= lambda x: x.cost)
            total_fitness: float = 0.0
            for plant in plants_and_buds:
                plant.fitness = 1.0 / plant.cost
                total_fitness += plant.fitness
            for plant in plants_and_buds:
                plant.p = plant.fitness / total_fitness
            random_numbers = [random.random() for _ in range(100)]
            plants = []
            for random_number in random_numbers:
                accumulated_probability = 0
                for i, plant in enumerate(plants_and_buds):
                    accumulated_probability += plant.p
                    if accumulated_probability >= random_number:
                        plants.append(plants_and_buds[i])
                        break
                    
            winner = sorted(plants, key= lambda x: x.cost)[0]
            print(winner.cost)
