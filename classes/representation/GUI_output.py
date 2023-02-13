from datetime import datetime

SCHEDULE_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DAILY_SHIFTS = {'shift 0': {'string': '730 - 1200'}, 'shift 1': {'string': '1200 - 1730'}}
EMPLOYEE_PER_SHIFT = 1

def shift_to_datetime(shift):
    start, end = shift.split(" - ")
    start_time = datetime.strptime(start, "%H%M").time()
    end_time = datetime.strptime(end, "%H%M").time()
    return start_time, end_time

def get_duration(datetime_list):
    start, end = datetime_list
    duration = datetime.combine(datetime.today(), end) - \
               datetime.combine(datetime.today(), start)
    return duration


# Add new keys with data
for shift in DAILY_SHIFTS:

    # Represent shift times in datetime objects
    DAILY_SHIFTS[shift]['datetime'] = list(shift_to_datetime(DAILY_SHIFTS[shift]['string']))

    # Calculate the duration of a given shift in datetime object
    DAILY_SHIFTS[shift]['duration'] = get_duration(DAILY_SHIFTS[shift]['datetime'])