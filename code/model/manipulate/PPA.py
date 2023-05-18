from itertools import chain
import random

from model.representation.behaviour_classes.malus_calc import MalusCalc
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.schedule import AbsSchedule, Plant
from model.representation.behaviour_classes.shift_constraints import Shiftconstraints
from model.manipulate.mutate import Mutate
from presenter.helpers import recursive_copy

class PPA:
    def __init__(self, start_schedule: AbsSchedule, **kwargs) -> None:
        self.Schedule = start_schedule
        self.NUMBER_OF_PLANTS = int(kwargs['num_plants'])
        self.NUMBER_OF_GENERATIONS = int(kwargs['num_gens'])
        self.employee_list = kwargs['employees']
        self.shift_list = kwargs['shifts']
        self.standard_cost = MalusCalc.get_standard_cost(self.employee_list)
        self.shiftconstraints = kwargs['shiftconstraints']
        self.temperature = float(kwargs['temperature'])
        self.mutate = Mutate(kwargs['employees'], kwargs['shifts'], self.standard_cost, self.shiftconstraints)        
        self.kwargs = kwargs

    def grow(self) -> None:
        ''' this is the core of the PPA algo. If adjust mutations is not activated it appears to find faster and 
            more consistent results... But maybe for larger data it does not. Check with Haarlemmermeer data'''
        winners = []

        # generate plants
        plants = self.gen_plants(self.Schedule, self.NUMBER_OF_PLANTS, self.standard_cost)
        lowest = plants[0]
        # print(lowest.cost)
        
        # run the PPA
        for _ in range(self.NUMBER_OF_GENERATIONS):
            self.temperature = PPA.adjust_temperature(self.temperature)

            # make mutations 
            plants_and_buds = list(chain(*[self.mutate.mutate(plant, self.temperature) for plant in plants]))

            # Calculate fitness values
            fitness_values = [1 / plant.cost for plant in plants_and_buds]

            # select plants based off fitness
            plants = [PPA.fitness_proportionate_selection(plants_and_buds, fitness_values) for _ in range(self.NUMBER_OF_PLANTS)]
            # change the number of mutations each plant gets
            plants = sorted(plants, key=lambda x: MalusCalc.compute_cost(self.standard_cost, x, plants))
            winners.append(plants[0]) 
            plants = PPA.adjust_mutations(plants)

            
            if winners[-1].cost < lowest.cost:
                lowest = winners[-1]
                        
            if len(winners) > 5:
                del winners[0]

            # reheating scheme
            if all(x == winners[0] for x in winners):
                self.temperature += 0.1 if self.temperature < 0.5 else + 0
            # print(MalusCalc.compute_cost(self.standard_cost, winners[-1]))

        ''' REVIEW ERROR LATER '''
        print(f'COST: {lowest.cost}')
        # for shift_id, employee_id in lowest.items():

        #     print(self.id_shift[shift_id], self.id_employee[employee_id])
        #     print(MalusCalc._compute_cost(winners[0].Workload, shift_id, employee_id), winners[0].Workload[employee_id])
        #     print("---------------")

        return lowest

    @staticmethod
    def fitness_proportionate_selection(plants: list[Plant], fitness_values: list[float]) -> Plant:
        total_fitness = sum(fitness_values)
        rel_fitnesses = [fitness / total_fitness for fitness in fitness_values]

        spin = random.random()  # spin the wheel
        for i, rel_fitness in enumerate(rel_fitnesses):
            spin -= rel_fitness
            if spin <= 0:
                return plants[i]

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

    def gen_plants(self, schedule: AbsSchedule, number_plants: int, standard_cost: float) -> list[Plant]:
        plants = []
        gen = True
        for _ in range(number_plants):
            plants.append(
                Plant(
                    Workload = Workload(self.shift_list, self.employee_list, set_workload=recursive_copy(schedule.Workload)),
                    cost = MalusCalc.compute_cost(standard_cost, schedule, gen),
                    set_schedule = recursive_copy(schedule)
                )
            )
        return plants

    @staticmethod
    def adjust_temperature(T: float) -> float:
        return T*0.90
