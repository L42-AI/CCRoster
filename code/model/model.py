from tqdm import tqdm

from model.data.assign import employee_list, shift_list

from model.representation.data_classes.schedule import AbsSchedule, Schedule
from model.representation.data_classes.workload import Workload
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift
from model.representation.data_classes.availability import Availability
from model.representation.data_classes.current_availabilities import CurrentAvailabilities

from model.manipulate.fill import Fill, Greedy
from model.manipulate.PPA import PPA

class Model:

    """ DATABASE """
    def get_offline_data():
        return shift_list, employee_list
    
    def download(location_id):
        ...
    
    """ SCHEDULE """


    def get_standard_cost(employee_list: list[Employee]) -> float:
        total = sum([employee.get_minimal_hours() * employee.get_wage()  for employee in employee_list])
        return round(total, 2)

    def get_time_conflict_dict(shift_list: list[Shift]) -> dict[int, set[int]]:
        time_conflict_dict = {shift.id: set() for shift in shift_list}
        for i, shift_1 in enumerate(shift_list):

            for shift_2 in shift_list[i+1:]:
                if shift_1.end < shift_2.start:
                    continue
                if shift_1.start < shift_2.end:
                    time_conflict_dict[shift_1.id].add(shift_2.id)
                    time_conflict_dict[shift_2.id].add(shift_1.id)

        return time_conflict_dict

    def _possible_shift(workable_shift: Availability, employee: Employee, shift: Shift) -> bool:

        # Check time
        if workable_shift.start > shift.start or workable_shift.end < shift.end:
            return False

        # Check task
        tasks_list = employee.get_tasks()
        for task in tasks_list:
            if task == shift.task:
                return True
        return False

    def _employee_availability(shift: Shift, employee_list: list[Employee]) -> set[int]:
        """
        this method is only used to develop the generator, later, the info will actually be downloaded
        for now it just returns a hardcoded list with availability
        """

        availabilities = set()
        for employee in employee_list:
            for weeknum in employee.availability_dict:
                for workable_shift in employee.availability_dict[weeknum]:

                    if Model._possible_shift(workable_shift, employee, shift):
                        availabilities.add(employee.id)

        return availabilities

    def get_all_availabilities(employee_list: list[Employee], shift_list: list[Shift]):
        return {shift.id: Model._employee_availability(shift, employee_list) for shift in shift_list}

    """ GEN SCHEDULE """

    def create_random_schedule():
        return Fill.fill(AbsSchedule(Workload()))

    def create_greedy_schedule(employee_list: list[Employee], shift_list: list[Shift]):
        all_availabilities = Model.get_all_availabilities(employee_list, shift_list)
        return Greedy.fill(employee_list, shift_list, Schedule(Workload(), CurrentAvailabilities(all_availabilities)))

    def propagate(employee_list: list[Employee], shift_list: list[Shift], **kwargs):
        schedule = Fill.fill(AbsSchedule(Workload()))
        # schedule = Greedy.fill(employee_list, shift_list, Schedule(Workload(), CurrentAvailabilities()))
        P = PPA(schedule, int(kwargs['num_plants']), int(kwargs['num_gens']))
        P.grow(float(kwargs['temperature']))

    def optimal(employee_list: list[Employee], shift_list: list[Shift], **kwargs):
        all_availabilities = Model.get_all_availabilities(employee_list, shift_list)

        fail = 0
        for _ in tqdm(range(10000)):
            try:
                schedule = Greedy.fill(employee_list, shift_list, Schedule(Workload(), CurrentAvailabilities(Model.recursive_copy(all_availabilities))))
            except:
                print('fail')
                fail += 1
        
        fail_propotion = fail / 10000
        print(fail_propotion)
        return schedule
    
    def recursive_copy(obj: object) -> object:

        if isinstance(obj, dict):
            return {k: Model.recursive_copy(v) for k, v in obj.items()}

        elif isinstance(obj, set):
            return {Model.recursive_copy(x) for x in obj}

        elif isinstance(obj, list):
            return [Model.recursive_copy(x) for x in obj]
        
        else:
            # final return
            return obj