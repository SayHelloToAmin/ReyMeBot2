import mysql.connector

from datetime import datetime

# Connect to MySQL Server :
db = mysql.connector.connect(
    host='localhost',
    user="root",
    password="KhodeAmin",
    database="reymebot",
    # auth_plugin='mysql_native_password'

)

Cursor = db.cursor()



# ====================== Check if User Id is exist in Database=====================

def CheckUserID(userid):
    Cursor.execute(f"SELECT USERNAMES from status WHERE userid = {userid}")
    Cloud = Cursor.fetchone()
    if Cloud:
        return True
    else:
        return False


# =======================Register User=============================================

def registeruser(NickName, user_id):
    try:
        Cursor.execute("INSERT INTO status (usernames,userid,count) VALUES (%s , %s , %s)", (NickName, user_id, 0))
        db.commit()
        Cursor.execute("INSERT INTO level (username , userid) VALUES (%s , %s)",(NickName,user_id))
        db.commit()
    except:
        return False
    else:
        return True


# =================================Count Messages and XP================================================

# this function only count messages of each user and add XP

def counter(user_id):
    Cursor.execute(f"""UPDATE status 
                    SET SCORE = SCORE + 0.25 , COUNT = COUNT + 1
                    WHERE USERID = {user_id} """)
    db.commit()
    Cursor.execute(f"""UPDATE level 
                    SET XP = XP + 1 WHERE userid = {user_id} """)


# ===================================Get Score====================================

# this functions just return a number

def give_score(userid):

    Cursor.execute(f"SELECT SCORE FROM status WHERE USERID = {userid}")
    Cloud = Cursor.fetchone()

    return Cloud[0]


# =================================== SET SCORE ============================================


# this function will set the new values of score

def setscore(userid, value):

    Cursor.execute("UPDATE status SET SCORE = %s WHERE USERID = %s", (value, userid))
    db.commit()



# ======================================Error recorder===========================================


# this function can record the randomly errors

def error_reporter(userid, description):

    current_datetime = datetime.now()
    current_datetime_formatted = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO error (Describtion , userid , date) VALUES (%s , %s , %s)"
    val = (description, userid, current_datetime_formatted)
    Cursor.execute(sql, val)
    db.commit()




#========================================Rank=======================================================


# this function return True if userid = ADMIN

def checkrank(userid):

    Cursor.execute(f"SELECT RANKED FROM status WHERE USERID = {userid}")
    Cloud = Cursor.fetchone()
    if Cloud[0] == "ADMIN":

        return True
    else:

        return False


#===============================================get level================================================

#this function return a number wich that level of user

def getlevel(userid):
    Cursor.execute(f"SELECT level FROM level WHERE userid = {userid}")
    Cloud = Cursor.fetchone()
    return Cloud[0]



#================================================get xp and xp needed====================================================

#this function weill return the xp value

def getxp(userid):
    Cursor.execute(f"SELECT xp,needed_xp FROM level WHERE userid = {userid}")
    Cloud = Cursor.fetchall()
    #return a tuple
    return Cloud
