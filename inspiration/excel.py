import pandas as pd
import random

""" Constraints """

def open_close(schedule):

    closer = schedule[list(schedule.keys())[-1:][0]][1]

    for day in schedule:
        opener = schedule[day][0]
        if opener != 'Empty':
            if opener == closer:
                return True
        closer = schedule[day][1]
    return False

def dubble_shift(schedule):
    for day in schedule:
        if schedule[day][0] != 'Empty' or schedule[day][1] != 'Empty':
            if schedule[day][0] == schedule[day][1]:
                return True
    return False

""" Create data """

def create_shifts_dict(av_dict):
    shifts = {}
    shifts['Shifts.1'] = []
    shifts['Shifts.2'] = []
    shifts['Shifts.3'] = []
    shifts['Shifts.4'] = []

    shifts['Recieved'] = []
    for employee in av_dict:
        shifts['Shifts.1'].append(av_dict[employee]['Shifts.1'])
        shifts['Shifts.2'].append(av_dict[employee]['Shifts.2'])
        shifts['Shifts.3'].append(av_dict[employee]['Shifts.3'])
        shifts['Shifts.4'].append(av_dict[employee]['Shifts.4'])
        shifts['Recieved'].append(av_dict[employee]['Recieved'])
    return shifts

def data_structures(df):

    schedule = {'Maandag.1': ['Empty', 'Empty'],
                'Dinsdag.1': ['Empty', 'Empty'],
                'Woensdag.1': ['Empty', 'Empty'],
                'Donderdag.1': ['Empty', 'Empty'],
                'Vrijdag.1': ['Empty', 'Empty'],
                'Zaterdag.1': ['Empty', 'Empty'],
                'Zondag.1': ['Empty', 'Empty'],
                'Maandag.2': ['Empty', 'Empty'],
                'Dinsdag.2': ['Empty', 'Empty'],
                'Woensdag.2': ['Empty', 'Empty'],
                'Donderdag.2': ['Empty', 'Empty'],
                'Vrijdag.2': ['Empty', 'Empty'],
                'Zaterdag.2': ['Empty', 'Empty'],
                'Zondag.2': ['Empty', 'Empty'],
                'Maandag.3': ['Empty', 'Empty'],
                'Dinsdag.3': ['Empty', 'Empty'],
                'Woensdag.3': ['Empty', 'Empty'],
                'Donderdag.3': ['Empty', 'Empty'],
                'Vrijdag.3': ['Empty', 'Empty'],
                'Zaterdag.3': ['Empty', 'Empty'],
                'Zondag.3': ['Empty', 'Empty'],
                'Maandag.4': ['Empty', 'Empty'],
                'Dinsdag.4': ['Empty', 'Empty'],
                'Woensdag.4': ['Empty', 'Empty'],
                'Donderdag.4': ['Empty', 'Empty'],
                'Vrijdag.4': ['Empty', 'Empty'],
                'Zaterdag.4': ['Empty', 'Empty'],
                'Zondag.4': ['Empty', 'Empty']}

    days_list = df.index.tolist()
    for i in range(4):
        days_list.remove(f'Shifts.{i + 1}')

    av_dict = {}
    for person in df[df.columns[1:]]:
        av_dict[person] = df[person].to_dict()
        av_dict[person]['Recieved'] = 0

    return schedule, days_list, av_dict

""" Select """

def select_employee(av_dict):
    # Create a dictionary with some key-value pairs
    shifts_dict = {}
    for employee in av_dict:
        shifts_dict[employee] = av_dict[employee]['Recieved']

    # Get the 4 lowest values in the dictionary
    values = sorted(shifts_dict.values())[:3]

    # Get the key-value pairs from the dictionary
    pairs = shifts_dict.items()

    # Filter the pairs to only include the ones with a value in the sorted list of values
    filtered_pairs = [pair for pair in pairs if pair[1] in values]

    # Extract the keys from the filtered pairs
    keys = [pair[0] for pair in filtered_pairs]

    return random.choice(keys)

def select_day(days_list) -> str:
    return random.choice(days_list)

""" Create """

def create_schedule(days_list, av_dict, schedule):

    count = 0
    no_shift_left = {}

    for employee in av_dict:
        no_shift_left[employee] = {'Shifts.1': False, 'Shifts.2': False, 'Shifts.3': False, 'Shifts.4': False}

    schedule_complete = False

    while schedule_complete == False:

        # Set emplyee and day for random schedules
        employee = select_employee(av_dict)
        day = select_day(days_list)

        # Set shift of week
        for i in range(4):
            if day[-2:] == f'.{i + 1}':
                shifts = f'Shifts.{i + 1}'

        if day.startswith('Z'):
            while employee not in ['Sophie', 'Isabella', 'Alex', 'Pim', 'Danaë', 'Miranda', 'Tamar']:
                employee = select_employee(av_dict)

        # If emplyee has no shifts left:
        if av_dict[employee][shifts] <= 0:

            if no_shift_left[employee][shifts] == True:
                continue

            no_shift_left[employee][shifts] = True
            continue

        # If employee has availability for the day
        if av_dict[employee][day] != 0:
            if schedule[day][0] == 'Empty' and (av_dict[employee][day] == 1 or av_dict[employee][day] == 3):

                schedule[day][0] = employee

                if open_close(schedule):
                    schedule[day][0] = 'Empty'
                elif dubble_shift(schedule):
                    schedule[day][0] = 'Empty'
                else:
                    if av_dict[employee][day] == 3:
                        av_dict[employee][day] = 2
                    else:
                        av_dict[employee][day] = 0

                    av_dict[employee][shifts] -= 1
                    av_dict[employee]['Recieved'] += 1
            elif schedule[day][1] == 'Empty' and (av_dict[employee][day] == 2 or av_dict[employee][day] == 3):

                schedule[day][1] = employee

                if open_close(schedule):
                    schedule[day][1] = 'Empty'
                elif dubble_shift(schedule):
                    schedule[day][1] = 'Empty'
                else:
                    if av_dict[employee][day] == 3:
                        av_dict[employee][day] = 1
                    else:
                        av_dict[employee][day] = 0

                    av_dict[employee][shifts] -= 1
                    av_dict[employee]['Recieved'] += 1

        if schedule[day][0] != 'Empty' and schedule[day][1] != 'Empty':
            if len(days_list) == 1:
                schedule_complete = True
                continue
            days_list.remove(day)

        count += 1

        if count == 10000:
            break

    return av_dict, schedule

if __name__ == '__main__':

    print()

    beschikbaarheid_df = pd.read_excel('Beschikbaarheid.xlsx', index_col=0)

    schedule_count = 0

    with pd.ExcelWriter('roosters.xlsx', engine='openpyxl') as writer:

        while schedule_count != 10:

            complete = True

            schedule, days_list, av_dict = data_structures(beschikbaarheid_df)

            av_dict, made_schedule = create_schedule(days_list, av_dict, schedule)

            for day in made_schedule:
                if made_schedule[day][0]  == 'Empty' or made_schedule[day][1] == 'Empty':
                    complete = False

            if complete == False:
                continue


            schedule_count += 1

            print('\nSCHEDULE:')
            print('================================================')
            print(made_schedule)
            print('================================================\n')

            df_finished = pd.DataFrame.from_dict(made_schedule)
            df_finished['index'] = ['Opener', 'Sluiter']
            df_finished.set_index(['index'], inplace=True)

            shifts = create_shifts_dict(av_dict)
            df_shifts = pd.DataFrame(shifts, index=av_dict.keys())

            df_finished = pd.concat((df_finished.T, df_shifts))

            df_finished.to_excel(writer, sheet_name=str(schedule_count))