from random import shuffle, choice
# class Solver():

#     def __init__(self):
#         self.ConstraintList = []
#         self.ConstraintOrder = self.ConstraintList

# solver = Solver()
# solver.ConstraintOrder.append(1)
# print(solver.ConstraintList)

class Job():
    def __init__(self, final_starting_time):
        self.final_starting_time = final_starting_time

class Patient():
    def __init__(self, jobs: list):
        self.jobs = jobs

actions = []

patient_list = []
for j in range(3):
    job_list = []
    for i in range(3):
        job = Job(i)
        job_list.append(job)
    patient_list.append(Patient(job_list))
shuffle(patient_list)

for patient in patient_list:
    
    
