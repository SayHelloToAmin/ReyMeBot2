import mysql.connector
import traceback
from etc import reporter
from datetime import datetime

# Connect to MySQL Server :
db = mysql.connector.connect(
    host='localhost',
    user="farhadb1_farhadb1",
    password="KhodeAminHastam",
    database="farhadb1_Reyme",
    # auth_plugin='mysql_native_password'

)

Cursor = db.cursor()



# ====================== Check if User Id is exist in Database=====================

def CheckUserID(userid):
    try:

        Cursor.execute(f"SELECT USERNAMES from status WHERE userid = {userid}")
        Cloud = Cursor.fetchone()
        if Cloud:
            return True
        else:
            return False
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)


# =======================Register User=============================================

def registeruser(NickName, user_id):
    try:
        try:
            Cursor.execute("INSERT INTO status (usernames,userid) VALUES (%s , %s )", (NickName, user_id))
            db.commit()
        except:
            return False
        else:
            return True
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,user_id)


# =================================Count Messages and XP================================================

# this function only count messages of each user and add XP

def counter(user_id):
    try:
        Cursor.execute(f"""UPDATE status 
                        SET SCORE = SCORE + 0.25 , COUNT = COUNT + 1
                        WHERE USERID = {user_id} """)
        db.commit()
        Cursor.execute(f"""UPDATE status 
                        SET xp = xp + 1 WHERE userid = {user_id} """)
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,user_id)


# ===================================Get Score====================================

# this functions just return a number

def give_score(userid):
    try:
        Cursor.execute(f"SELECT SCORE FROM status WHERE USERID = {userid}")
        Cloud = Cursor.fetchone()

        return Cloud[0]
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)


# =================================== SET SCORE ============================================


# this function will set the new values of score

def setscore(userid, value):
    try:
        Cursor.execute("UPDATE status SET SCORE = %s WHERE USERID = %s", (value, userid))
        db.commit()
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)



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
    try:
        Cursor.execute(f"SELECT RANKED FROM status WHERE USERID = {userid}")
        Cloud = Cursor.fetchone()
        if Cloud[0] == "ADMIN":
            return True
        else:
            return False
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)

#===============================================get level================================================

#this function return a number wich that level of user

def getlevel(userid):
    try:
        Cursor.execute(f"SELECT level FROM status WHERE userid = {userid}")
        Cloud = Cursor.fetchone()
        return Cloud[0]
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)


#================================================get xp and xp needed====================================================

#this function weill return the xp value

def getxp(userid):
    try:
        Cursor.execute(f"SELECT xp,needed_xp FROM status WHERE userid = {userid}")
        Cloud = Cursor.fetchall()
        #return a tuple
        return Cloud[0]
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)


#===========================================set new needed_xp================================================================

#this function could update the needed_xp

def upneedxp(userid):
    try:
        Cursor.execute(f"""UPDATE status 
                        SET needed_xp = needed_xp * 1.2 
                        WHERE USERID = {userid} """)
        return True
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)



#====================================================set new xp=================================================================

#this function could update the xp

def upxp(userid,value):
    try:
        Cursor.execute("""UPDATE status 
                        SET xp = %s
                        WHERE USERID = %s """,(value,userid))
        return True
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)




#====================================================add one level=================================================================

#this function could update the level

def uplevel(userid):
    try:
        Cursor.execute(f"""UPDATE status 
                        SET level = level + 1
                        WHERE USERID = {userid} """)
        return True
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)



#====================================================reduc one level=================================================================

#this function could update the level

def downlevel(userid):
    try:
        Cursor.execute(f"""UPDATE status 
                        SET level = level - 1
                        WHERE USERID = {userid} """)
        return True
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)