import mysql.connector
import traceback
from etc.reporter import exceptf
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
        Cursor.execute(f"SELECT ID from status WHERE userid = {userid}")
        Cloud = Cursor.fetchone()
        if Cloud:
            return True
        else:
            return False



# =======================Register User=============================================

def registeruser(NickName, user_id):
        try:
            Cursor.execute("INSERT INTO status (usernames,userid) VALUES (%s , %s )", (NickName, user_id))
            db.commit()
        except:
            return False
        else:
            return True



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
        db.commit()
    except Exception as e:
        tb = e.__traceback__
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,user_id)


# ===================================Get Score====================================

# this functions just return a number

def give_score(userid):
    try:
        Cursor.execute(f"SELECT SCORE FROM status WHERE USERID = {userid}")
        Cloud = Cursor.fetchone()

        return Cloud[0]
    except Exception as e:
        tb = e.__traceback__
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)


# =================================== SET SCORE ============================================


# this function will set the new values of score

def setscore(userid, value):
    try:
        Cursor.execute("UPDATE status SET SCORE = %s WHERE USERID = %s", (value, userid))
        db.commit()
    except Exception as e:
        tb = e.__traceback__
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)



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
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)

#===============================================get level================================================

#this function return a number wich that level of user

def getlevel(userid):
    try:
        Cursor.execute(f"SELECT level FROM status WHERE userid = {userid}")
        Cloud = Cursor.fetchone()
        return Cloud[0]
    except Exception as e:
        tb = e.__traceback__
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)


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
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)


#===========================================set new needed_xp================================================================

#this function could update the needed_xp

def upneedxp(userid):
    try:
        Cursor.execute(f"""UPDATE status 
                        SET needed_xp = needed_xp * 1.2 
                        WHERE USERID = {userid} """)
        db.commit()
        return True
    except Exception as e:
        tb = e.__traceback__
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)



#====================================================set new xp=================================================================

#this function could update the xp

def upxp(userid,value):
    try:
        Cursor.execute("""UPDATE status 
                        SET xp = %s
                        WHERE USERID = %s """,(value,userid))
        db.commit()
    except Exception as e:
        tb = e.__traceback__
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)




#====================================================add one level=================================================================

#this function could update the level

def uplevel(userid):
    try:
        Cursor.execute(f"""UPDATE status 
                        SET level = level + 1
                        WHERE USERID = {userid} """)
        db.commit()
    except Exception as e:
        tb = e.__traceback__
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)



#====================================================reduc one level=================================================================

#this function could update the level

def downlevel(userid):
    try:
        Cursor.execute(f"""UPDATE status 
                        SET level = level - 1
                        WHERE USERID = {userid} """)
        db.commit()
        return True
    except Exception as e:
        tb = e.__traceback__
        exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name ,userid)


#==========================================================set lottery point and number==============================================

# this function just update lottery point and more details

async def lotterysetter(mydic,namedic):
    for username , np in mydic.items():
        Cursor.execute(f"""UPDATE status 
                        SET wins = wins + 1
                        WHERE userid = {namedic[username]} """)
        db.commit()
        Cloud = np.split("-")
        Cloud1 = int(Cloud[0])
        Cloud2 = int(Cloud[1])
        if Cloud1 == 1:
            Cursor.execute("""UPDATE status 
                        SET onenum = onenum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 2:
            Cursor.execute("""UPDATE status 
                        SET twonum = twonum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 4:
            Cursor.execute("""UPDATE status 
                        SET fournum = fournum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 5:
            Cursor.execute("""UPDATE status 
                        SET fivenum = fivenum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 6:
            Cursor.execute("""UPDATE status 
                        SET jackpot = jackpot + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 3:
            Cursor.execute("""UPDATE status 
                        SET threenum = threenum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()





#======================================================username updater======================================================

def upname(userid,name):
    Cursor.execute("UPDATE status SET usernames = %s WHERE USERID = %s", (name, userid))
    db.commit()