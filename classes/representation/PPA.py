import random
from itertools import chain

from classes.representation.malus_calc import MalusCalc
from classes.representation.generator import Generator
from classes.representation.schedule import Schedule
from classes.representation.workload import Workload
from classes.representation.schedule import Schedule
from classes.representation.malus_calc import MalusCalc
from helpers import recursive_copy, id_employee, id_shift

class PPA:
    def __init__(self, num_plants: int, num_gens: int, TEMPERATURE: float=.5) -> None:
        self.G = Generator()
        self.Schedule = self.G.Schedule # not necessary but better readability imo
        self.NUMBER_OF_PLANTS = num_plants
        self.NUMBER_OF_GENERATIONS = num_gens
        self.id_employee = id_employee
        self.id_shift = id_shift
        self.grow(TEMPERATURE)

    def grow(self, temperature: float) -> None:
        winners = []
        plants = PPA.gen_plants(self.Schedule, self.NUMBER_OF_PLANTS)
        lowest = plants[0]
        
        for _ in range(self.NUMBER_OF_GENERATIONS):
            temperature = PPA.adjust_temperature(temperature)

            plants_and_buds = list(chain(*[self.G.mutate(plant, temperature) for plant in plants]))
            plants = [PPA.tournament_selection(plants_and_buds, temperature) for _ in range(self.NUMBER_OF_PLANTS)]
            best_plant = sorted(plants, key=lambda x: MalusCalc.compute_final_costs(self.G.standard_cost, x))[0]
            winners.append(best_plant)
            if best_plant.cost < lowest.cost:
                lowest = best_plant
                        
            if len(winners) > 5:
                del winners[0]

            if all(x == winners[0] for x in winners):
                temperature += 0.1 if temperature < 0.5 else + 0
            print(MalusCalc.compute_final_costs(self.G.standard_cost, winners[-1]))

        print(f'COST: {lowest.cost}')
        for shift_id, employee_id in lowest.items():

            print(self.id_shift[shift_id], self.id_employee[employee_id])
            print(MalusCalc._compute_cost(winners[0].Workload, shift_id, employee_id), winners[0].Workload[employee_id])
            print("---------------")

    @staticmethod
    def tournament_selection(plants: list[Schedule], T: float, k: int = 5) -> Schedule:  # k is the tournament size
        selected_plants = random.sample(plants, k)
        winner = min(selected_plants, key=lambda x: x.cost)
        return winner

    @staticmethod
    def gen_plants(schedule: Schedule, number_plants: int) -> list[Schedule]:
        plants = []
        for _ in range(number_plants):
            plants.append(
                Schedule(
                    Workload = Workload(recursive_copy(schedule.Workload)),
                    cost = schedule.cost,
                    set_schedule = recursive_copy(schedule)
                )
            )
        return plants

    @staticmethod
    def adjust_temperature(T: float) -> float:
        return T*0.90
