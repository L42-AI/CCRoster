import random
import numpy as np

from model.representation.data_classes import (
    Availability, Employee, Shift)


def gen_id_dict(l: list[object]) -> dict[int, object]:
    try:
        l[0].id
    except:
        raise AttributeError('List contents have no ID attribute')
    
    return {x.id : x for x in l}

def gen_time_conflict_dict(shift_list: list[Shift]) -> dict[int, set[int]]:
    time_conflict_dict = {shift.id: set() for shift in shift_list}
    for i, shift_1 in enumerate(shift_list):

        for shift_2 in shift_list[i+1:]:
            if shift_1.end < shift_2.start:
                continue
            if shift_1.start < shift_2.end:
                time_conflict_dict[shift_1.id].add(shift_2.id)
                time_conflict_dict[shift_2.id].add(shift_1.id)

    return time_conflict_dict

def get_standard_cost(employee_list: list[Employee]) -> float:
    total = sum([employee.get_minimal_hours() * employee.get_wage()  for employee in employee_list])
    return round(total, 2)

def get_random_shift_id(shift_list: list[Shift]) -> int:
    return random.choice(shift_list).id

def get_random_employee_id(total_availabilities: dict[int, set[int]], shift_id: int, existing_employee: int = None) -> int:
    """
    returns an employee id
    """

    if existing_employee != None:
        choices = total_availabilities[shift_id] - {existing_employee}
    else:
        choices = total_availabilities[shift_id]
    
    if not choices:
        raise ValueError("No available employees for shift")

    return random.choice(list(choices))

def recursive_copy(obj: object) -> object:

    if isinstance(obj, dict):
        return {k: recursive_copy(v) for k, v in obj.items()}

    elif isinstance(obj, set):
        return {recursive_copy(x) for x in obj}

    elif isinstance(obj, list):
        return [recursive_copy(x) for x in obj]
    
    else:
        # final return
        return obj



def _possible_shift(workable_shift: Availability, employee: Employee, shift: Shift) -> tuple[bool, int]:

    # Check time
    start_gap = shift.start - workable_shift.start
    end_gap = workable_shift.end - shift.end

    if not (start_gap.days or end_gap.days) == 0 :
        return False, -999

    closeness = start_gap.seconds + end_gap.seconds

    # Check task
    tasks_list = employee.get_tasks()
    for task in tasks_list:
        if task == shift.task:
            # return True, int((round(closeness / 10000, 0)))
            return True, 1
    return False, -999

def _employee_availability(shift: Shift, employee_list: list[Employee]) -> set[int]:
    """
    this method is only used to develop the generator, later, the info will actually be downloaded
    for now it just returns a hardcoded list with availability
    """

    availabilities = {}
    for employee in employee_list:
        for weeknum in employee.availability_dict:
            for workable_shift in employee.availability_dict[weeknum]:

                possibility = _possible_shift(workable_shift, employee, shift)
                if possibility[0]:
                    if employee.id not in availabilities:
                        availabilities[employee.id] = possibility[1]

    return availabilities

def gen_total_availabilities(employee_list: list[Employee], shift_list: list[Shift]) -> dict[int, set[int]]:
    return {shift.id: _employee_availability(shift, employee_list) for shift in shift_list}

def compute_prob(score: float, total: float) -> float:
    """
    Normalize a score based on a part and a total.

    Args:
        score: The score to be normalized.
        total: The total score.

    Returns:
        The normalized score.
    """
    if total == 0:
        return 1.0

    normalized_score = (score / total)
    return normalized_score


def softmax_function(lst):
    """
    Apply the softmax function to a list of floats.

    Args:
        lst (list): A list of floats.

    Returns:
        list: The softmax values of the input list.

    """
    # Convert the input list to a numpy array
    arr = np.array(lst)

    # Apply the softmax function
    softmax_values = np.exp(arr) / np.sum(np.exp(arr))

    # Return the softmax values as a list
    return softmax_values.tolist()

def improved_softmax_function(lst):
    """
    Apply the softmax function to a list of floats while handling zeros.

    If the input list contains a zero at a specific index, the function will return
    zero at the same index while softmaxing the rest of the values.

    Args:
        lst (list): A list of floats.

    Returns:
        list: The softmax values of the input list, with zeros preserved.

    """
    # Convert the input list to a numpy array
    arr = np.array(lst)

    # Find the indices of zeros in the input array
    zero_indices = np.where(arr == 0)[0]

    # Remove zeros from the array for softmax calculation
    arr_without_zeros = np.delete(arr, zero_indices)

    # Apply the softmax function to the array without zeros
    softmax_values_without_zeros = np.exp(arr_without_zeros) / np.sum(np.exp(arr_without_zeros))

    # Initialize the output array with zeros
    output = np.zeros_like(arr)

    # Assign softmax values to the corresponding indices in the output array
    output_without_zeros = np.zeros_like(arr_without_zeros)
    output_without_zeros[...] = softmax_values_without_zeros
    output[np.delete(np.arange(len(arr)), zero_indices)] = output_without_zeros

    # Return the output array as a list
    return output.tolist()

