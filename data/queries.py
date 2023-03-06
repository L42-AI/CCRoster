import mysql
# http://wouterverdegaal.com:8080/
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
def downloading_employees(db, cursor):
    '''
    downloading all active employees from one location
    '''
    query = 'SELECT FROM Employee'
def uploading_shifts(db, cursor, entry):
    '''
    uploading shifts needed
    '''

    query = 'INSERT INTO Shifts (day, start, end, task, location) VALUES (%s, %s, %s, %s, %s)'
    values = (entry[0], entry[1], entry[2], entry[3], entry[4])
    cursor.execute(query, values)
    db.commit()

def downloading_shifts(db, cursor, location):
    '''
    downloading the shifts that need to be filled
    '''
    query = 'SELECT week, day, start, end, task FROM Shifts WHERE location = %s'
    value = (location,) # hardcoded for cc
    cursor.execute(query, value)
    rows = cursor.fetchall()
    return rows

def downloading_availability(db, cursor, location):
    '''
    downloading the availability per location
    '''
    # hardcoded 1 resembling coffeecompany
    query = 'SELECT * FROM Availability WHERE employee_id IN (SELECT id from Employee WHERE location=%s)'
    value = (location,) # for now location is always 1
    cursor.execute(query, value)
    rows = cursor.fetchall() # this selects the info into a list with tuples corresponding with rows
    # print(f'rows: {rows}')
    return rows

def get_task(db, cursor, id):
    query = 'SELECT task FROM Employee WHERE id=%s'
    value = [id]
    cursor.execute(query, value)
    return cursor.fetchone()[0]

def employee_per_shift(db, cursor, shift):
    '''
    returns all compatible employees for a shift
    '''

    query = 'SELECT id, hourly FROM Employee WHERE id IN (SELECT employee_id FROM Availability WHERE week = %s AND day = %s AND shift = %s AND employee_id IN (SELECT id FROM Employee WHERE task = %s))'
    values = (shift[0], shift[1], shift[2], shift[3])
    cursor.execute(query, values)
    return cursor.fetchall()

def download_wages(db, cursor, location):
    '''
    method generates a dictionary with employee id as key and their wage as value.
    can be used in malus calc to quickly get wages per employee, independend of local data but
    directly from server
    '''

    wage_dict = {}
    query = 'SELECT id, hourly FROM Employee WHERE location = %s'
    values = ([location])
    cursor.execute(query, values)

    # fill the dictionary
    for x in cursor:
        id, wage = x
        wage_dict[id] = wage
    return wage_dict