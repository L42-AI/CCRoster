import mysql.connector

'''
step 1: ga naar https://dev.mysql.com/downloads/installer/ en download het grootste bestand. Je moet geen acc aanmaken, onderaan staat best klein install without signing in
step 2: run de wizard, maak een ww aan en onthoud die (je moet wanneer je kan kiezen tussen ww de grootste mogelijkheid nemen)
step 3: probeer dit te runnen, wellicht werkt t. Wanneer je het runt, check docstrings vd functies
step 4: als t niet werkt, run in je terminal pip install mysql-connector-python en eventueel pip install mysql
step 5: probeer het nog een keer
step 6: werkt het nog niet? janken. Check de video van tech with tim: https://www.youtube.com/watch?v=3vsC05rxZ8c
'''

def setup():
    db = mysql.connector.connect(
        host='localhost',
        user='jacob',
        passwd='rooster'
        )

    mycursor = db.cursor() # dit is een class die te vergelijken is met hoe wij sqlite gebruikte, hierin type je je commands
    mycursor.execute('CREATE DATABASE testrooster')
    db.commit() # commit is nodig wanneer je wat aan de db toevoegd, dus niet als je een een berekening doet of wat opvraagt


def fill():
    '''
    run deze jongen om wat tabellen te maken in je lokale sql database. let op: dit is nog geen server,
    je creeert alleen een kopie van wat ik ook lokaal heb staan op mn laptop
    '''

    db = mysql.connector.connect(
        host='localhost', # niet veranderen
        user='jacob',
        passwd='rooster',
        database='testrooster' # niet veranderen
        )

    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE Employee (name VARCHAR(50), hourly SMALLINT, level SMALLINT, id INT PRIMARY KEY AUTO_INCREMENT)")
    mycursor.execute("CREATE TABLE Availability (employeeID INT PRIMARY KEY, FOREIGN KEY(employeeID) REFERENCES Employee(id), day VARCHAR(50), start SMALLINT, end SMALLINT)")
    mycursor.execute("CREATE TABLE schedule (day VARCHAR(10), start SMALLINT, end SMALLINT, employeeID INT PRIMARY KEY, FOREIGN KEY(employeeID) REFERENCES Employee(id))")
    db.commit()

    mycursor.execute("DESCRIBE Employee") # hiermee haal je info op uit je db, en zet die niet in je terminal zoals wij deden met sqlite, maar je zet het in de class
    for x in mycursor: # vandaar dat je over je cursor heen moet loopen
        print(x)

def drop():
    db = mysql.connector.connect(
        host='localhost', # niet veranderen
        user='jacob',
        passwd='rooster',
    )

    mycursor = db.cursor()
    mycursor.execute("SHOW DATABASES")
    databases = mycursor.fetchall() 
    if ('testrooster',) in databases:
        mycursor.execute('DROP DATABASE testrooster')
        db.commit()

    db.close()

drop()
setup()
fill()