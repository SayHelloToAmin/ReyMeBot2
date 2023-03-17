from mysql.connector import connection

#Connect to MySQL Server : 
db = connection.MySQLConnection(
    host = '127.0.0.1',
    user = "root",
    password = "KhodeAmin",
    database = "reymebot"


)

db.close()





#====================== Check if User Id is exist in Database=====================

def CheckUserID(userid):
    Cursor = db.cursor()
    db.connect()
    Cursor.execute(f"SELECT ID from status WHERE user_id = {userid}")
    Cloud = Cursor.fetchone()
    if Cloud:
        db.close()
        return True
    else:
        db.close()
        return False
    
#=======================Register User=============================================

def registeruser(NickName,user_id):
    Cursor = db.cursor()
    db.connect()
    try:
        Cursor.execute(f"INSERT INTO STATUS (usernames , user_id ) VALUES ({NickName},{user_id})")
        db.commit()
    except:
        db.close()
        return False
    else:
        db.close()
        return True

