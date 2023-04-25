import random
import itertools

from classes.representation.generator import Generator
from classes.representation.workload import Workload
from classes.representation.schedule import Schedule
from classes.representation.malus_calc import MalusCalc
from helpers import get_shift, get_employee, recursive_copy, get_temperature

from data.assign import employee_list, shift_list, total_availabilities

class PlantPropagation:
    def __init__(self, num_plants: int, num_gens: int, TEMPERATURE=.5) -> None:
        self.gen: Generator = Generator()
        self.Schedule = self.gen.Schedule # not necessary but better readability imo
        self.NUMBER_OF_PLANTS: int = num_plants
        self.NUMBER_OF_GENERATIONS: int = num_gens
        self.T: int = TEMPERATURE

        self.grow()


    def grow(self):
        winners = []
        plants = [Schedule(Workload(recursive_copy(self.Schedule.Workload)), self.Schedule.cost, recursive_copy(self.Schedule)) for i in range(self.NUMBER_OF_PLANTS)]
        for _ in range(self.NUMBER_OF_GENERATIONS):
            self.T = get_temperature(self.T)
            plants_and_buds = [self.gen.mutate(plant, self.T) for plant in plants]
            plants_and_buds = list(itertools.chain(*plants_and_buds))

            def tournament_selection(plants, k=5):  # k is the tournament size
                selected_plants = random.sample(plants, k)
                if random.random() < self.T:  # Occasionally select a plant with worse cost
                    winner = max(selected_plants, key=lambda x: x.cost)
                else:
                    winner = min(selected_plants, key=lambda x: x.cost)
                return winner

            plants = [tournament_selection(plants_and_buds) for _ in range(self.NUMBER_OF_PLANTS)]
            winners.append(sorted(plants, key=lambda x: MalusCalc.compute_final_costs(self.gen.standard_cost, x))[0])
            if len(winners) > 5:
                del winners[0]
            # print([x.cost for x in winners])
            if all(x == winners[0] for x in winners):
                self.T += 0.1 if self.T < 0.5 else + 0

            print(MalusCalc.compute_final_costs(self.gen.standard_cost, winners[0]))
        winners = sorted(plants, key= lambda x: x.cost)
        for shift_id, employee_id in winners[0].items():

            print(get_shift(shift_id), get_employee(employee_id))
            print(MalusCalc._compute_cost(winners[0].Workload, shift_id, employee_id), winners[0].Workload[employee_id])
            print("---------------")
        
