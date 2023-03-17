from mysql.connector import connection

#Connect to MySQL Server : 
db = connection.MySQLConnection(
    host = '127.0.0.1',
    user = "root",
    password = "KhodeAmin",
    database = "reymebot"


)

Cursor = db.cursor() #=========> Thats What We Need In All Of DataBase's Requests