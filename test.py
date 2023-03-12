from datetime import date, timedelta

def get_last_day_of_month(months_into_future: int = 0):
    today = date.today()
    last_day_of_month = today.replace(month=today.month + months_into_future + 1, day=1) - timedelta(1)
    return last_day_of_month


def get_monday(last_day_of_month):
    first_monday_of_next_month = last_day_of_month + timedelta(days=(7-last_day_of_month.weekday()))
    return first_monday_of_next_month


last_day_of_current_month = get_last_day_of_month()
last_day_of_next_month = get_last_day_of_month(months_into_future=1)

start_day = get_monday(last_day_of_current_month)
end_day = get_monday(last_day_of_next_month)

print(start_day)
print(end_day)