import random

class Employee:
    def __init__(self, name, av, exp) -> None:
        self.name = name
        self.availability = av
        self.expertise = exp

    def get_av(self):
        return random.choice(self.availability)

    def get_name(self):
        return self.name