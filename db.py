from mysql.connector import connection
from etc import Count
from datetime import datetime

# Connect to MySQL Server :
db = connection.MySQLConnection(
    host='localhost',
    user="root",
    password="0918",
    database="reymebot"

)

Cursor = db.cursor()
db.close()


# ====================== Check if User Id is exist in Database=====================

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


# =======================Register User=============================================

def registeruser(NickName, user_id):
    db.connect()
    try:
        Cursor.execute("INSERT INTO STATUS (usernames,userid,count) VALUES (%s , %s , %s)", (NickName, user_id, 0))
        db.commit()
    except:
        db.close()
        return False
    else:
        db.close()
        return True


# =================================SHOW SCORE=================================================

# this function only count messages of each user

def counter(user_id):
    db.connect()
    Cursor.execute(f"""UPDATE STATUS 
                    SET SCORE = SCORE + 0.5 , COUNT = COUNT + 1
                    WHERE USERID = {user_id} """)
    db.commit()
    db.close()


# ===================================Get Score====================================

# this functions just return a number

def givecount(userid):
    db.connect()
    Cursor.execute(f"SELECT SCORE FROM STATUS WHERE USERID = {userid}")
    Cloud = Cursor.fetchone
    db.close()
    return Cloud[0]


# =================================== SET SCORE ============================================


# this function will set the new values of score

def setscore(userid, value):
    db.connect()
    Cursor.execute("UPDATE STATUS SET SCORE = %s WHERE USERID = %s", (value, userid))
    db.commit()
    db.close()


# ======================================Error recorder===========================================


# this function can record the randomly errors

def error_reporter(userid, description):
    db.connect()
    current_datetime = datetime.now()
    current_datetime_formatted = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO error (Describtion , userid , date) VALUES (%s , %s)"
    val = (description, userid, current_datetime_formatted)
    Cursor.execute(sql, val)
    db.commit()
