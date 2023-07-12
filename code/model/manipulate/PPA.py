from itertools import chain
import random

from model.representation.data_classes.current_availabilities import CurrentAvailabilities
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.schedule import Schedule, Plant

from model.representation.behaviour_classes import MalusCalc
from model.manipulate import mutate

from helpers import recursive_copy, gen_total_availabilities

class PPA:
    def __init__(self, start_schedule: Schedule) -> None:
        self.Schedule = start_schedule
        self.id_employee = start_schedule.Workload.id_employee
        self.id_shift = start_schedule.Workload.id_shift

    def grow(self, config: dict[str, str]) -> None:
        ''' this is the core of the PPA algo. If adjust mutations is not activated it appears to find faster and 
            more consistent results... But maybe for larger data it does not. Check with Haarlemmermeer data'''
        
        temperature = float(config['temperature'])
        NUM_PLANTS = int(config['num_plants'])
        NUM_GENERATIONS = int(config['num_gens'])
        
        winners = []

        # generate plants
        plants = PPA.gen_plants(self.Schedule, NUM_PLANTS)
        lowest = plants[0]
        
        # run the PPA
        for _ in range(NUM_GENERATIONS):
            temperature = PPA.adjust_temperature(temperature)

            # make mutations 
            plants_and_buds = list(chain(*[mutate(plant, temperature) for plant in plants]))

            # select plants based off fitness
            plants = [PPA.tournament_selection(plants_and_buds, temperature) for _ in range(NUM_PLANTS)]

            # change the number of mutations each plant gets
            plants = sorted(plants, key=lambda schedule: MalusCalc.compute_cost(schedule))
            winners.append(plants[0])            
            plants = PPA.adjust_mutations(plants)

            
            if winners[-1].cost < lowest.cost:
                lowest = winners[-1]
                        
            if len(winners) > 5:
                del winners[0]

            # reheating scheme
            if all(x == winners[0] for x in winners):
                temperature += 0.1 if temperature < 0.5 else + 0
            print(MalusCalc.compute_cost(winners[-1]))

        ''' REVIEW ERROR LATER '''
        # print(f'COST: {lowest.cost}')
        # for shift_id, employee_id in lowest.items():

        #     print(self.id_shift[shift_id], self.id_employee[employee_id])
        #     print(MalusCalc._compute_cost(winners[0].Workload, shift_id, employee_id), winners[0].Workload[employee_id])
        #     print("---------------")

        return lowest

    @staticmethod
    def tournament_selection(plants: list[Plant], T: float, tournement_size: int = 5) -> Plant:
        selected_plants = random.sample(plants, tournement_size)
        winner = min(selected_plants, key=lambda x: x.cost)
        return winner
    
    @staticmethod
    def adjust_mutations(plants: list[Plant]) -> list[Plant]:
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
    def gen_plants(schedule: Schedule, number_plants: int) -> list[Plant]:
        
        employee_list = schedule.Workload.employee_list
        shift_list = schedule.Workload.shift_list
        
        plants = []
        for _ in range(number_plants):
            plants.append(
                Plant(
                    Workload(employee_list, shift_list, recursive_copy(schedule.Workload)),
                    CurrentAvailabilities(gen_total_availabilities(employee_list, shift_list)),
                    MalusCalc.compute_cost(schedule),
                    recursive_copy(schedule)
                )
            )
        return plants

    @staticmethod
    def adjust_temperature(temp: float) -> float:
        return temp * .9
