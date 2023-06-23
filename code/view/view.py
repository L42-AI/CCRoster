from pprint import pprint
import matplotlib.pyplot as plt

import numpy as np

from model.representation.data_classes.schedule import Schedule
from model.representation.data_classes.employee import Employee
from model.representation.data_classes.shift import Shift

class View:
    def print_schedule(schedule: Schedule, id_employee_dict: dict[int, Employee], id_shift_dict: dict[int, Shift]):
        for shift_id, employee_id in schedule.items():
            print(id_shift_dict.get(shift_id, None), id_employee_dict.get(employee_id, None))

    def print_success_rate(invalid_schedules: list[Schedule], valid_schedules: list[Schedule]):
        def count_unique_elements(lst):
            unique_elements = []
            for item in lst:
                if item not in unique_elements:
                    unique_elements.append(item)
            return len(unique_elements)

        print('Success factor:', len(valid_schedules) / (len(valid_schedules) + len(invalid_schedules)))
        print('Amount of unique arangements:', count_unique_elements(valid_schedules))

    def plot_schedules(valid_counts: dict[int, dict[int, int]], invalid_counts: dict[int, dict[int, int]], colors: list[str]):
        """
        Generate a barplot with multiple colors within each bar based on data composition.

        Args:
            groups (list): List of groups/labels for each bar.
            values_list (list): List of value lists for each group/bar.
            colors_list (list): List of color lists for each group/bar.

        Returns:
            None (displays the barplot).
        """

        print(len(valid_counts))

        # Generate bar plots for each shift assignment count
        fig, axes = plt.subplots(3, 9, figsize=(16, 8))
        fig.tight_layout(pad=3.0)
        
        View._plot(axes, invalid_counts, colors[0])
        View._plot(axes, valid_counts, colors[1], bottom=invalid_counts)
        
        # Show the plot
        # plt.show()

    def _plot(axes: np.ndarray, counts: dict[int, dict[int, int]], color: str, bottom: dict[int, dict[int, int]] = None):
        def calc_bottom(shift_id: int, bottom: dict[int, dict[int, int]]) -> list[int]:
            if shift_id not in bottom:
                return [0]
            elif isinstance(bottom[shift_id], int):
                return [bottom[shift_id]]
            else:
                return list(bottom[shift_id].values())
            
        
        for shift_id, shift_counts in counts.items():
            ax: plt.Axes = axes[shift_id // 9, shift_id % 9]
            
            if bottom:
                bar_bottom = calc_bottom(shift_id, bottom)
            else:
                bar_bottom = [0] * len(shift_counts)

            # Create a stacked bar chart
            ax.bar([name[0] for name in shift_counts.keys()], shift_counts.values(), bottom=bar_bottom, color=color)
            ax.set_xlabel('Employee ID')
            ax.set_ylabel('Occurrences')
            ax.set_title(f'Shift {shift_id + 1}')

