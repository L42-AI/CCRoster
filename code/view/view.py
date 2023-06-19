from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

from helpers import recursive_copy

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
    
    def split_valid_schedules(schedules: list[Schedule]) -> tuple[list[Schedule], list[Schedule]]:
        def has_none_values(data_dict: dict):
            for value in data_dict.values():
                if value is None:
                    return True
            return False

        shift_count_dict = {shift_id: {} for shift_id in schedules[0]}

        valid_schedules = []
        invalid_schedules = []

        for schedule in schedules:

            for shift_id, employee_id in schedule.items():
                if employee_id not in shift_count_dict[shift_id]:
                    shift_count_dict[shift_id][str(employee_id)] = 0

            if has_none_values(schedule):
                invalid_schedules.append(schedule)
            else:
                valid_schedules.append(schedule)
        
        return invalid_schedules, valid_schedules, shift_count_dict

    def process_data(schedules: list[Schedule], shift_count_dict: dict[int, dict[int, int]]) -> dict[int, dict[int, int]]:

        for schedule in schedules:
            for shift_id, employee_id in schedule.items():
                shift_count_dict[shift_id][str(employee_id)] += 1

        return shift_count_dict

    def plot(axes: np.ndarray, counts: dict[int, dict[int, int]], color: str, bottom: dict[int, dict[int, int]] = None):
        for shift_id, shift_counts in counts.items():
            ax = axes[shift_id // 9, shift_id % 9]
            
            if bottom:
                bar_bottom = View.calc_bottom(shift_id, bottom)
            else:
                bar_bottom = [0] * len(shift_counts)

            # Create a stacked bar chart
            ax.bar(shift_counts.keys(), shift_counts.values(), bottom=bar_bottom, color=color)

    def calc_bottom(shift_id: int, bottom: dict[int, dict[int, int]]) -> list[int]:
            if shift_id not in bottom:
                return [0]
            elif isinstance(bottom[shift_id], int):
                return [bottom[shift_id]]
            else:
                return list(bottom[shift_id].values())
            
    def multi_color_barplot(schedules: list[Schedule], colors: list[str]):
        """
        Generate a barplot with multiple colors within each bar based on data composition.

        Args:
            groups (list): List of groups/labels for each bar.
            values_list (list): List of value lists for each group/bar.
            colors_list (list): List of color lists for each group/bar.

        Returns:
            None (displays the barplot).
        """
        
        invalid_schedules, valid_schedules, shift_count_dict = View.split_valid_schedules(schedules)

        View.print_success_rate(invalid_schedules, valid_schedules)

        invalid_counts = View.process_data(invalid_schedules, recursive_copy(shift_count_dict))
        valid_counts = View.process_data(valid_schedules, recursive_copy(shift_count_dict))

        # Generate bar plots for each shift assignment count
        fig, axes = plt.subplots(3, 9, figsize=(16, 8))
        fig.tight_layout(pad=3.0)
        
        View.plot(axes, invalid_counts, colors[0])
        View.plot(axes, valid_counts, colors[1], bottom=invalid_counts)
        
        # Show the plot
        plt.show()

    def print_success_rate(invalid_schedules: list[Schedule], valid_schedules: list[Schedule]):
        
        def count_unique_elements(lst):
            unique_elements = []
            for item in lst:
                if item not in unique_elements:
                    unique_elements.append(item)
            return len(unique_elements)

        print('success factor:', len(valid_schedules) / (len(valid_schedules) + len(invalid_schedules)))
        print('Amount of unique arangements:', count_unique_elements(valid_schedules))


