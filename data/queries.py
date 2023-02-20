import mysql

def db_cursor():
    db = mysql.connector.connect(
                host="185.224.91.162",
                port=3308,
                user="Jacob",
                password="wouterisdebestehuisgenoot",
                database="rooster" # niet veranderen
            )
    cursor = db.cursor()
    return db, cursor

datalist = [] # this is the list like we discussed

def uploading_shifts(db, cursor):
    '''
    uploading shifts needed
    '''
    for entry in datalist:
        query = 'INSERT INTO Shifts (day, start, end, task, location) VALUES (%s, %s, %s, %s, %s)'
        values = (entry[0], entry[1], entry[2], entry[3], entry[4])
        cursor.execute(query, values)
    db.commit()

def downloading_shifts(db, cursor):
    '''
    downloading the shifts that need to be filled
    '''
    query = 'SELECT day, start, end, task FROM Shifts WHERE location = %s'
    value = (1) # hardcoded for cc
    cursor.execute(query, value)
    rows = cursor.fetchall()
    return rows

def downloading_availability(db, cursor):
    '''
    downloading the availability per location
    '''
    # hardcoded 1 resembling coffeecompany
    query = 'SELECT * FROM Availability WHERE location = %s'
    value = (1) # for now location is always 1
    cursor.execute(query, value)
    rows = cursor.fetchall() # this selects the info into a list with tuples corresponding with rows
    return rows
