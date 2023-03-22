
class MalusCalc:
    def wage_cost(schedule) -> int:
        total_cost = 0
        for shift, employee in schedule:
            cost = shift.duration * employee.get_wage()
            total_cost += cost
        return total_cost