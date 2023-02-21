import mysql.connector

db = mysql.connector.connect(
                host="185.224.91.162",
                port=3308,
                user="Jacob",
                password="wouterisdebestehuisgenoot",
                database="rooster" # niet veranderen
            )
cursor = db.cursor()

query = 'SELECT * FROM Availability WHERE employee_id IN (SELECT id from Employee WHERE location=%s)'
value = [1] # for now location is always 1
cursor.execute(query, value)
for x in cursor:
    print(x)










import numpy as np

zero = np.zeros((20, 4))

rows = [(1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1), 
        (1, 1, 1, 1),]
print(zero)
for _, row in enumerate(rows):
    zero[_] = row
print()
print(zero)