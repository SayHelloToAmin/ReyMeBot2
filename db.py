from mysql.connector import connection

#Connect to MySQL Server : 
db = connection.MySQLConnection(
    host = '127.0.0.1',
    user = "root",
    password = "KhodeAmin",
    database = "reymebot"


)

Cursor = db.cursor() #=========> Thats What We Need In All Of DataBase's Requests

db.close()





#====================== Check if User Id is exist in Database=====================

def CheckUserID(userid):
    db.connect()
    try:
        Cursor.execute(f"SELECT id from status WHERE user_id = {userid}")
    except:
        db.close()
        return False
    else:
        db.close()
        return True
