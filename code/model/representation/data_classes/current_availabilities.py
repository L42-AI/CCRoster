class CurrentAvailabilities(dict):
    def __init__(self):
        from model.representation.behaviour_classes.schedule_constants import total_availabilities
        for shift_id, shift_availability in total_availabilities.items():
            self[shift_id] = [0, shift_availability]