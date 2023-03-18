import mysql.connector
from etc import Count
from datetime import datetime
import traceback
from etc import reporter

# Connect to MySQL Server :
db = mysql.connector.connect(
    host='localhost',
    user="root",
    password="KhodeAmin",
    database="reymebot"
    # auth_plugin='mysql_native_password'

)

Cursor = db.cursor()
db.close()


# ====================== Check if User Id is exist in Database=====================

def CheckUserID(userid):
    try:
        db.connect()
        Cursor.execute(f"SELECT USERNAMES from status WHERE userid = {userid}")
        Cloud = Cursor.fetchone()
        if Cloud:
            db.close()
            return True
        else:
            db.close()
            return False
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name)


# =======================Register User=============================================

def registeruser(NickName, user_id):
    try:
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
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name)


# =================================SHOW SCORE=================================================

# this function only count messages of each user

def counter(user_id):
    try:
        db.connect()
        Cursor.execute(f"""UPDATE STATUS 
                        SET SCORE = SCORE + 0.5 , COUNT = COUNT + 1
                        WHERE USERID = {user_id} """)
        db.commit()
        db.close()
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name)


# ===================================Get Score====================================

# this functions just return a number

def givescore(userid):
    try:
        db.connect()
        Cursor.execute(f"SELECT SCORE FROM STATUS WHERE USERID = {userid}")
        Cloud = Cursor.fetchone
        db.close()
        return Cloud[0]
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name)


# =================================== SET SCORE ============================================


# this function will set the new values of score

def setscore(userid, value):
    try:
        db.connect()
        Cursor.execute("UPDATE STATUS SET SCORE = %s WHERE USERID = %s", (value, userid))
        db.commit()
        db.close()
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name)


# ======================================Error recorder===========================================


# this function can record the randomly errors

def error_reporter(userid, description):
    try:
        db.connect()
        current_datetime = datetime.now()
        current_datetime_formatted = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO error (Describtion , userid , date) VALUES (%s , %s)"
        val = (description, userid, current_datetime_formatted)
        Cursor.execute(sql, val)
        db.commit()
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name)





#==============================================Check Rank=================================================


# this function just return True (ADMIN) , and False (USER)

def checkrank(userid):
    try:
        db.connect()
        Cursor.execute(f"SELECT RANKED FROM STATUS WHERE userid = {userid}")
        Cloud = Cursor.fetchone()
        if Cloud == "ADMIN":
            db.close()
            return True
        else:
            db.close()
            return False
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name)