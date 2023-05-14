from itertools import chain
import random

from model.representation.malus_calc import MalusCalc
from model.representation.schedule import Plant, Schedule
from model.representation.workload import Workload
from model.representation.current_availabilities import CurrentAvailabilities

from model.improve.mutate import mutate
from model.improve.fill import Greedy

from model.data.schedule_constants import standard_cost
from helpers import recursive_copy, id_employee, id_shift

class PPA:
    def __init__(self, num_plants: int, num_gens: int, TEMPERATURE: float=.8) -> None:
        self.Schedule = Schedule(Workload(), 99999, CurrentAvailabilities())
        # self.Schedule = Greedy.greedy_fill(self.Schedule)
        self.standard_cost = standard_cost
        self.NUMBER_OF_PLANTS = num_plants
        self.NUMBER_OF_GENERATIONS = num_gens
        self.session_id = session_id
        self.id_employee, self.id_shift = self.id_objects()
        self.grow(TEMPERATURE)

    def id_objects(self):
        employee_list = download_employees(self.session_id)
        shift_list = download_shifts(self.session_id)
        id_employee = {x.id: x for x in employee_list}
        id_shift = {x.id: x for x in shift_list}

        return id_employee, id_shift
 
    def grow(self, temperature: float) -> None:
        winners = []
        plants = PPA.gen_plants(self.Schedule, self.NUMBER_OF_PLANTS)
        lowest = plants[0]
        
        for _ in range(self.NUMBER_OF_GENERATIONS):
            temperature = PPA.adjust_temperature(temperature)

            plants_and_buds = list(chain(*[mutate(plant, temperature) for plant in plants]))
            plants = [PPA.tournament_selection(plants_and_buds, temperature) for _ in range(self.NUMBER_OF_PLANTS)]
            best_plant = sorted(plants, key=lambda x: MalusCalc.compute_cost(self.standard_cost, x))[0]
            winners.append(best_plant)

            if best_plant.cost < lowest.cost:
                lowest = best_plant
                        
            if len(winners) > 5:
                del winners[0]

            if all(x == winners[0] for x in winners):
                temperature += 0.1 if temperature < 0.5 else + 0
            print(MalusCalc.compute_cost(self.standard_cost, winners[-1]))

        print(f'COST: {lowest.cost}')
        for shift_id, employee_id in lowest.items():

            print(self.id_shift[shift_id], self.id_employee[employee_id])
            print(self.id_employee[employee_id].weekly_max)
            print(lowest.Workload[employee_id])
            # print(MalusCalc._compute_cost(winners[0].Workload, shift_id, employee_id), winners[0].Workload[employee_id])
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
                Plant(
                    Workload = Workload(recursive_copy(schedule.Workload)),
                    cost = schedule.cost,
                    set_schedule = recursive_copy(schedule),
                    CurrentAvailabilities = CurrentAvailabilities()
                )
            )
        return plants

    @staticmethod
    def adjust_temperature(T: float) -> float:
        return T*0.90
