import mysql

db = mysql.connector.connect(
            host="185.224.91.162",
            port=3308,
            user="Jacob",
            password="wouterisdebestehuisgenoot",
            database="rooster" # niet veranderen
        )
cursor = db.cursor()

datalist = [] # this is the list like we discussed

for entry in datalist:
    query = 'INSERT INTO Shifts (day, start, end, task, location) VALUES (%s, %s, %s, %s, %s)'
    values = (entry[0], entry[1], entry[2], entry[3], entry[4])
    cursor.execute(query, values)
db.commit()
