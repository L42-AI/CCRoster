
class MalusCalc:
    def wage_cost(schedule, shifts_id_dict, employees_id_dict) -> int:
        total_cost = 0
        for shift_id, employee_id in schedule:
            cost = shifts_id_dict[shift_id].duration * employees_id_dict[employee_id].get_wage()
            total_cost += cost
        return total_cost

    def total_costs(schedule, employees):
        """
        calculates the total costs of a schedule
        """
        # calculate the starting costs
        total = sum([sum(x.weekly_min.values()) * x.get_wage()  for x in employees])

        # add the shift costs
        total += sum(x[2] for x in schedule)

        return total
