import mysql.connector
# import pymysql

print('Loading')

# db = pymysql.connect(host="http://wouterverdegaal.com",
#                      port=8080,
#                      user="Jacob",
#                      passwd="wouterisdebestehuisgenoot",
#                      database="rooster")
db = mysql.connector.connect(
        host='http://wouterverdegaal.com', # niet veranderen
        port=8080,
        user='Jacob',
        passwd='wouterisdebestehuisgenoot',
        database='rooster' # niet veranderen
        )

print('Loading')
cursor = db.cursor()
cursor.execute('INSERT INTO Employee (name, hourly, level, task, location) VALUES ("Karel", 20, 1, 1, 0)')
print('inserting')
db.commit()
print('Done')