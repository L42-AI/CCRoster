import random
from classes.representation.generator import Generator


class Plant(Generator):
    def __init__(self, schedule: dict[int, int], P: int) -> None:
        self.schedule = schedule
        self.sim_an = P # probability of accpeting worsening of cost
        self.improve(200)
        
    """ MUTATE """

    def mutate(self):
        '''
        makes mutations to the schedule but remembers original state and returns to it if
        change is not better. So no deepcopies needed :0
        '''
        replace_shift_id = self.__get_random_shift()

        current_employee_id = self.schedule[replace_shift_id]
        replace_employee_id = self.__get_random_employee(replace_shift_id, current_employee_id)

        current_cost = Generator.get_total_cost()

        if self.__check_workload_capacity(replace_shift_id, replace_employee_id):

            if Generator.passed_hard_constraints(replace_shift_id, replace_employee_id):
                # print('improvement')
                self.schedule_swap(replace_shift_id, replace_employee_id)
                        
            # leave a bad change with probability of self.sim_an
            if Generator.get_total_cost() > current_cost and random.random() > self.sim_an:

                self.schedule_swap(replace_shift_id, current_employee_id)
        
        else:

            # try to 'ease' workers workload by having someone else take over the shift, store the changes 
            undo_update = self.mutate_max_workload(replace_shift_id, replace_employee_id) 
           
            total_costs_new = Generator.get_total_cost()

            # compare costs
            if total_costs_new > current_cost and random.random() > self.sim_an:

                for shift_id, employee_id in undo_update:
                    # swap back
                    self.schedule_swap(shift_id, employee_id)

        
    def mutate_extra_employees(self) -> None:
        sorted_shifts = sorted(self.schedule.keys(), key = lambda shift_id: self.actual_availabilities[shift_id][1], reverse=True)

        for shift_id in sorted_shifts:
            for employee_id in self.actual_availabilities[shift_id][1]:
                if self.__check_workload_capacity(shift_id, employee_id):
                    ...
        return

    def mutate_max_workload(self, shift_to_replace_id: int, possible_employee_id: int) -> list[tuple[int, int]]:
        '''
        Method gets called when mutate wants to schedule a worker for a shift but the worker is already
        working his/hers max. This method will replace one of his/her shifts to check if that will be cheaper
        '''

        undo_update = []

        # get the shortest shift the busy person is working
        shortest_shift_id = sorted(self.shifts, key=lambda x: x.duration)[0].id

        if shift_to_replace_id == shortest_shift_id:
            return []

        # pick new employee to work the shortest shift
        shortest_shift_employee_id = self.__get_random_employee(shortest_shift_id, possible_employee_id)

        if self.__check_workload_capacity(shortest_shift_id, shortest_shift_employee_id):
            if Generator.passed_hard_constraints(shortest_shift_id, shortest_shift_employee_id):

                # store the changes ('old employee, shift')
                undo_update.append((shortest_shift_id, self.schedule[shortest_shift_id]))
                self.schedule_swap(shortest_shift_id, shortest_shift_employee_id)
        else:
            self.mutate_max_workload(shortest_shift_id, shortest_shift_employee_id)
        return undo_update

    
    def __get_random_shift(self) -> int:
        """
        returns a tuple with inside (1) a tuple containing shift info and (2) an index
        """

        shift_id = random.choice(self.shifts).id
        while len(self.availabilities[shift_id]) < 2:
            shift_id = random.choice(self.shifts).id
        return shift_id

    def __get_random_employee(self, shift_id: int, current_employee_id: int) -> int:
        """
        returns an employee id
        """
        current_employee_id = self.schedule[shift_id]

        choices = self.availabilities[shift_id] - {current_employee_id}
        if not choices:
            raise ValueError("No available employees for shift")
        return random.choice(list(choices))
    
    def __check_workload_capacity(self, shift_id: int, employee_id: int) -> bool:
        """
        returns True if the employee is allowed to work that shift given his/hers weekly max
        """

        employee_obj = self.get_employee(employee_id)

        # get the week and check how many shifts the person is working that week
        weeknumber = self.get_weeknumber(shift_id)

        if employee_obj.get_week_max(weeknumber) > (len(self.workload[employee_id][weeknumber])):
            return True
        else:
            # if the person will not take on the shift, delete it from the workload
            return False
        
    def schedule_swap(self, shift_id: int, employee_id: int) -> None:
        Generator.schedule_out(shift_id)
        Generator.schedule_in(shift_id, employee_id)

    

   