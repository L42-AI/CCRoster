from pprint import pprint
import matplotlib.pyplot as plt


from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

class View:
    def print_schedule(schedule: Schedule, id_employee_dict: dict[int, Employee], id_shift_dict: dict[int, Shift]):
        for shift_id, employee_id in schedule.items():
            print(id_shift_dict.get(shift_id, None), id_employee_dict.get(employee_id, None))
    
    def graph_schedules(schedules: list[Schedule]):
        
        # schedules = View.print_success_rate(schedules)
        
        # Initialize a dictionary to count the occurrences of employee assignments for each shift
        shift_counts = {shift_id: {} for shift_id in schedules[0]}

        # Count the occurrences of employee assignments for each shift
        for schedule in schedules:
            for shift_id, employee_id in schedule.items():
                if employee_id != None:
                    employee_id = employee_id + 1

                if str(employee_id) not in shift_counts[shift_id]:
                    shift_counts[shift_id][str(employee_id)] = 1
                else:
                    shift_counts[shift_id][str(employee_id)] += 1

        # Generate bar plots for each shift assignment count
        fig, axes = plt.subplots(3, 9, figsize=(16, 8))
        fig.tight_layout(pad=3.0)

        for shift_id in (shift_counts):
            ax = axes[shift_id // 9, shift_id % 9]
            occurrences = shift_counts[shift_id]
            bars = list(occurrences.keys())
            values = list(occurrences.values())
            print(values)
            colors = ["g" if value is not None else "r" for value in values]
            ax.bar(bars, values, color=colors)
            ax.set_xlabel('Shift ID')
            ax.set_ylabel('Occurrences')
            ax.set_title(f'Shift {shift_id + 1}')

        plt.show()
    
    def print_success_rate(schedules: list[Schedule]):
        def has_none_values(data_dict: dict):
            for value in data_dict.values():
                if value is None:
                    return True
            return False
        
        def count_unique_elements(lst):
            unique_elements = []
            for item in lst:
                if item not in unique_elements:
                    unique_elements.append(item)
            return len(unique_elements)

        success_schedules = []

        success = 0
        for schedule in schedules:
            if has_none_values(schedule):
                continue
            success += 1
            success_schedules.append(schedule)

        print('success factor:', success / len(schedules))
        print('Amount of unique arangements:', count_unique_elements(success_schedules))
        return success_schedules


