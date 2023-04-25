import random
from itertools import chain

from classes.representation.generator import Generator
from classes.representation.schedule import Schedule
from classes.representation.workload import Workload

from helpers import recursive_copy

class PlantPropagation:
    def __init__(self, num_plants: int, num_gens: int, TEMPERATURE: float=.8) -> None:
        self.G: Generator = Generator()
        self.G.greedy_fill()
        self.Schedule = self.G.Schedule # not necessary but better readability imo
        self.NUMBER_OF_PLANTS: int = num_plants
        self.NUMBER_OF_GENERATIONS: int = num_gens

        self.plants(TEMPERATURE)


    def plants(self, T: float):
        # plants = [Schedule(Workload(recursive_copy(self.Schedule.Workload)), self.Schedule.cost, recursive_copy(self.Schedule)) for i in range(100)]
        plants = [Schedule(Workload(recursive_copy(self.Schedule.Workload)), self.Schedule.cost, recursive_copy(self.Schedule)) for _ in range(100)]
        for _ in range(20):
            T = self.get_temperature(T)
            plants_and_buds = [self.G.mutate(plant, T) for plant in plants]
            plants_and_buds = self.flatten_list(plants_and_buds)
            plants_and_buds = sorted(plants_and_buds, key= lambda x: x.cost)

            self.assign_fitness(plants_and_buds)
            plants = self.bud_plants(plants_and_buds)
                    
            winner = sorted(plants, key= lambda x: x.cost)[0]
            print(winner.cost)

    @staticmethod
    def assign_fitness(plants_and_buds: list[Schedule]) -> None:
        total_fitness = 0.0
        for plant in plants_and_buds:
            plant.fitness = 1.0 / plant.cost
            total_fitness += plant.fitness

        for plant in plants_and_buds:
            plant.p = plant.fitness / total_fitness

    @staticmethod
    def bud_plants(plants_and_buds: list[Schedule]) -> list[Schedule]:
        plants = []
        random_numbers = [random.random() for _ in range(100)]
        for random_number in random_numbers:
            accumulated_probability = 0
            for i, plant in enumerate(plants_and_buds):
                accumulated_probability += plant.p
                if accumulated_probability >= random_number:
                    plants.append(plants_and_buds[i])
                    break

        return plants

    @staticmethod
    def flatten_list(l: list[list]) -> list[Schedule]:
        return list(chain(*l))

    @staticmethod
    def get_temperature(T):
        return T*0.80