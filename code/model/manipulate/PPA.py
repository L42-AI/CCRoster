from itertools import chain
import random

from model.representation.behaviour_classes.malus_calc import MalusCalc
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.schedule import AbsSchedule, Plant

from model.representation.behaviour_classes.schedule_constants import standard_cost
from model.manipulate.mutate import mutate
from helpers import recursive_copy, id_employee, id_shift

class PPA:
    def __init__(self, start_schedule: AbsSchedule, num_plants: int, num_gens: int, TEMPERATURE: float=.5) -> None:
        self.Schedule = start_schedule
        self.standard_cost = standard_cost
        self.NUMBER_OF_PLANTS = num_plants
        self.NUMBER_OF_GENERATIONS = num_gens
        self.id_employee = id_employee
        self.id_shift = id_shift

    def grow(self, adjust, temperature: float) -> None:
        ''' this is the core of the PPA algo. If adjust mutations is not activated it appears to find faster and 
            more consistent results... But maybe for larger data it does not. Check with Haarlemmermeer data'''
        winners = []

        # generate plants
        plants = PPA.gen_plants(self.Schedule, self.NUMBER_OF_PLANTS, self.standard_cost)
        lowest = plants[0]
        
        # run the PPA
        for _ in range(self.NUMBER_OF_GENERATIONS):
            temperature = PPA.adjust_temperature(temperature)

            # make mutations 
            plants_and_buds = list(chain(*[mutate(plant, temperature) for plant in plants]))

            # select plants based off fitness
            plants = [PPA.tournament_selection(plants_and_buds, temperature) for _ in range(self.NUMBER_OF_PLANTS)]

            # change the number of mutations each plant gets
            plants = sorted(plants, key=lambda x: MalusCalc.compute_cost(self.standard_cost, x))
            winners.append(plants[0]) 
            if adjust:           
                plants = PPA.adjust_mutations(plants)

            
            if winners[-1].cost < lowest.cost:
                lowest = winners[-1]
                        
            if len(winners) > 5:
                del winners[0]

            # reheating scheme
            if all(x == winners[0] for x in winners):
                temperature += 0.1 if temperature < 0.5 else + 0
            # print(MalusCalc.compute_cost(self.standard_cost, winners[-1]))

        ''' REVIEW ERROR LATER '''
        # print(f'COST: {lowest.cost}')
        # for shift_id, employee_id in lowest.items():

        #     print(self.id_shift[shift_id], self.id_employee[employee_id])
        #     print(MalusCalc._compute_cost(winners[0].Workload, shift_id, employee_id), winners[0].Workload[employee_id])
        #     print("---------------")

        return lowest

    @staticmethod
    def tournament_selection(plants: list[Plant], T: float, k: int = 5) -> Plant:  # k is the tournament size
        selected_plants = random.sample(plants, k)
        winner = min(selected_plants, key=lambda x: x.cost)
        return winner
    
    @staticmethod
    def adjust_mutations(plants)-> list[Plant]:
        ''' Fittest plants get fewer mutations, worse plants get few'''
        lenght = len(plants)
        for i, plant in enumerate(plants):
            decrease = 4 - (4 * i) // lenght  # Decreasing decrease amount
            plant.MUTATIONS = max(plant.MUTATIONS - decrease, 3)

        # Reverse the list to decrease the highest scores
        plants.reverse()  
        for i, plant in enumerate(plants):
            increase = 4 - (4 * i) // lenght  # Decreasing increase amount
            plant.MUTATIONS = min(plant.MUTATIONS + increase, 20)
        return plants

    @staticmethod
    def gen_plants(schedule: AbsSchedule, number_plants: int, standard_cost: float) -> list[Plant]:
        plants = []
        for _ in range(number_plants):
            plants.append(
                Plant(
                    Workload = Workload(recursive_copy(schedule.Workload)),
                    cost = MalusCalc.compute_cost(standard_cost, schedule),
                    set_schedule = recursive_copy(schedule)
                )
            )
        return plants

    @staticmethod
    def adjust_temperature(T: float) -> float:
        return T*0.90
