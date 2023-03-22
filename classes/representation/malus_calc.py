
class MalusCalc:
    def wage_cost(schedule) -> int:
        total_cost = 0
        for shift, employee in schedule:
            cost = shift.duration * employee.get_wage()
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
