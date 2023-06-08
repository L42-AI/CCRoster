class View:
    def print_schedule(schedule, id_employee_dict, id_shift_dict):
        for shift_id, employee_id in schedule.items():
            print(id_shift_dict[shift_id], id_employee_dict[employee_id])