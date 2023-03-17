from mysql.connector import connection
from etc import Count
#Connect to MySQL Server : 
db = connection.MySQLConnection(
    host = 'localhost',
    user = "root",
    password = "KhodeAmin",
    database = "reymebot"


)

Cursor = db.cursor()
db.close()




#====================== Check if User Id is exist in Database=====================

def CheckUserID(userid):
    db.connect()
    Cursor.execute(f"SELECT USERNAMES from status WHERE userid = {userid}")
    Cloud = Cursor.fetchone()
    if Cloud:
        db.close()
        return True
    else:
        db.close()
        return False
    
#=======================Register User=============================================

def registeruser(NickName,user_id):
    db.connect()
    try:
        Cursor.execute("INSERT INTO STATUS (usernames,userid,count) VALUES (%s , %s , %s)" , (NickName,user_id , 0))
        db.commit()
    except:
        db.close()
        return False
    else:
        db.close()
        return True



#=================================Count=================================================

#this function only count messages of each user

def counter(user_id):
    db.connect()
    Cursor.execute("""UPDATE STATUS
                    SET COUNT = COUNT+1
                        WHERE userid = %S """,(user_id))
    db.commit()
    db.close()    