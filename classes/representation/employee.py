import random

class Employee:
    def __init__(self, name, av, exp) -> None:
        self.name = name
        # self.availability = self.init_av(av)
        self.availability = av
        self.expertise = exp

    # def init_av(self, av):
    #     availability = set()

    #     return availability

    def get_av(self):
        return random.choice(self.availability)

    def get_name(self):
        return self.name