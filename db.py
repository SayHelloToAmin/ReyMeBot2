import mysql.connector
import traceback

from datetime import datetime

# Connect to MySQL Server :
db = mysql.connector.connect(
    host='localhost',
    user="root",
    password="amin1400",
    database="reymebot",
    # auth_plugin='mysql_native_password'

)

Cursor = db.cursor()



# ====================== Check if User Id is exist in Database=====================

def CheckUserID(userid):
        Cursor.execute(f"SELECT ID FROM statuss WHERE userid = {userid}")
        Cloud = Cursor.fetchone()
        if Cloud is None:
            return False
        else:
            return True


# =======================Register User=============================================

def registeruser(NickName, user_id):
        try:
            Cursor.execute("INSERT INTO statuss (usernames,userid) VALUES (%s,%s)", (NickName, user_id))
            db.commit()
        except:
            return False
        else:
            return True



# =================================Count Messages and XP================================================

# this function only count messages of each user and add XP

def counter(user_id):
        Cursor.execute(f"""UPDATE statuss 
                        SET SCORE = SCORE + 0.25 , COUNT = COUNT + 1
                        WHERE USERID = {user_id} """)
        db.commit()
        Cursor.execute(f"""UPDATE statuss 
                        SET xp = xp + 1 WHERE userid = {user_id} """)
        db.commit()



# ===================================Get Score====================================

# this functions just return a number

def give_score(userid):

        Cursor.execute(f"SELECT SCORE FROM statuss WHERE USERID = {userid}")
        Cloud = Cursor.fetchone()

        return Cloud[0]



# =================================== SET SCORE ============================================


# this function will set the new values of score

def setscore(userid, value):

        Cursor.execute("UPDATE statuss SET SCORE = %s WHERE USERID = %s", (value, userid))
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

        Cursor.execute(f"SELECT RANKED FROM statuss WHERE USERID = {userid}")
        Cloud = Cursor.fetchone()
        if Cloud[0] == "ADMIN":
            return True
        else:
            return False


#===============================================get level================================================

#this function return a number wich that level of user

def getlevel(userid):

        Cursor.execute(f"SELECT level FROM statuss WHERE userid = {userid}")
        Cloud = Cursor.fetchone()
        return Cloud[0]



#================================================get xp and xp needed====================================================

#this function weill return the xp value

def getxp(userid):

        Cursor.execute(f"SELECT xp,needed_xp FROM statuss WHERE userid = {userid}")
        Cloud = Cursor.fetchall()
        #return a tuple
        return Cloud[0]



#===========================================set new needed_xp================================================================

#this function could update the needed_xp

def upneedxp(userid):

        Cursor.execute(f"""UPDATE statuss 
                        SET needed_xp = needed_xp * 1.2 
                        WHERE USERID = {userid} """)
        db.commit()
        return True




#====================================================set new xp=================================================================

#this function could update the xp

def upxp(userid,value):

        Cursor.execute("""UPDATE statuss 
                        SET xp = %s
                        WHERE USERID = %s """,(value,userid))
        db.commit()




# ===================================================add one
# level=================================================================

#this function could update the level

def uplevel(userid):

        Cursor.execute(f"""UPDATE statuss 
                        SET level = level + 1
                        WHERE USERID = {userid} """)
        db.commit()




#====================================================reduc one level=================================================================

#this function could update the level

def downlevel(userid):

        Cursor.execute(f"""UPDATE statuss 
                        SET level = level - 1
                        WHERE USERID = {userid} """)
        db.commit()
        return True



#==========================================================set lottery point and number==============================================

# this function just update lottery point and more details

async def lotterysetter(mydic,namedic):
    for username , np in mydic.items():
        Cursor.execute(f"""UPDATE statuss 
                        SET wins = wins + 1
                        WHERE userid = {namedic[username]} """)
        db.commit()
        Cloud = np.split("-")
        Cloud1 = int(Cloud[0])
        Cloud2 = int(Cloud[1])
        if Cloud1 == 1:
            Cursor.execute("""UPDATE statuss 
                        SET onenum = onenum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 2:
            Cursor.execute("""UPDATE statuss 
                        SET twonum = twonum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 4:
            Cursor.execute("""UPDATE statuss 
                        SET fournum = fournum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 5:
            Cursor.execute("""UPDATE statuss 
                        SET fivenum = fivenum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 6:
            Cursor.execute("""UPDATE statuss 
                        SET jackpot = jackpot + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()
        elif Cloud1 == 3:
            Cursor.execute("""UPDATE statuss 
                        SET threenum = threenum + 1 , SCORE = SCORE + %s
                        WHERE userid = %s """,(Cloud2,namedic[username]))
            db.commit()




#======================================================username updater======================================================

def upname(userid,name):
    Cursor.execute("UPDATE statuss SET usernames = %s WHERE USERID = %s", (name, userid))
    db.commit()



#=========================================================get lottery status=======================================================

#def this functin will return a touple in the list that can return the user's information


async def lotterystatus(userid):
    Cursor.execute(f"SELECT wins,onenum,twonum,threenum,fournum,fivenum,jackpot FROM statuss WHERE userid = {userid}")
    Cloud = Cursor.fetchall()
    return Cloud[0]



#=====================================================mute log =======================================================================

#this function will record the mute history !
def muterecorder(userid_1,userid_2):
    #userid_1 kasi ke mute karde 
    #userid_2 kasi ke mute shode
    try:
        Cursor.execute("INSERT INTO mutes (byy,who,datee) VALUES (%s,%s,%s)",(userid_1,userid_2,datetime.now()))
        db.commit()
    except:
        Cursor.execute("""update mutes
        set much = much +1 , datee = %s where byy = %s and who = %s""",(datetime.now(),userid_1,userid_2))
        db.commit()
        
        
        
        
        
        
        
        
        
        
        
        
#====================================================muted by==========================================================================

#this function only return a number as count and last date 

def mutedby(userid1,userid2):
    Cursor.execute("""SELECT much , datee from mutes
where byy = %s and who = %s""",(userid2,userid1))
    Cloud = Cursor.fetchone()
    if not Cloud:
        return False
    else:
        return Cloud
    


##=====================================================muted========================================================================

#this function only return a number as count and last date 

def muted(userid1,userid2):
    Cursor.execute("""SELECT much , datee from mutes
where byy = %s and who = %s""",(userid1,userid2))
    Cloud = Cursor.fetchone()
    if not Cloud:
        return False
    else:
        return Cloud
    
    
    
    
    
    
    
#===============================================================top pm==========================================================

# this function will get an ordered touple with count and usernames

def gettoppm():
    Cursor.execute("""SELECT usernames , count from statuss
order by count desc
limit 8""")
    Cloud = Cursor.fetchall()
    return Cloud




#==========================================================ChatGPT counter==========================================

#this function only count the accepted answers of users

def countchatgpt(userid):
    Cursor.execute(f"""UPDATE statuss 
SET chatgpt = chatgpt + 1 WHERE USERID = {userid}""")
    db.commit()

#====================================================Record XO game count============================================

#this function only record games count

def xocount(*userid):
    for user in userid:
        Cursor.execute(f"""UPDATE statuss 
SET xo_games = xo_games + 1 WHERE USERID = {user}""")
    db.commit()
#========================================================Record XO result=============================================

#this function just record the result of XO games for each player

def recxo(userid1,userid2,wonmoney):
    # userid1 === > is that player who is the winner
    # userid2 === > is that player who is the loser
    #wonmoney === > that money the player1 won
    try:
        Cursor.execute("INSERT INTO xo_games (winner,loser,wonmoney) VALUES (%s,%s,%s)",(userid1,userid2,wonmoney))
        db.commit()
    except:
        Cursor.execute("""update xo_games
        set much = much +1 , wonmoney = wonmoney + %s where winner = %s and loser = %s""",(wonmoney,userid1,userid2))
        db.commit()


# ========================================== xo games and wins and loses ===============================================

# the following functions will return xo games , wins , loses the player in XO game!

# games
async def xogames(userid):
    Cursor.execute(f"SELECT xo_games FROM statuss where userid = {userid}")
    Cloud = Cursor.fetchone()
    return Cloud[0]

# wins
async def xowins(userid):
    Cursor.execute(f"""select sum(much) from xo_games where winner = {userid} 
group by winner""")
    Cloud = Cursor.fetchone()
    return Cloud[0]

#loses
async def xoloses(userid):
    Cursor.execute(f"""select sum(much) from xo_games where loser = {userid} 
group by winner""")
    Cloud = Cursor.fetchone()
    return Cloud[0]


#=================================================show winRate(xo) =======================================

#this function will return the player's winrate on XO

async def xo_winrate(userid):
    Cloud1 = await xogames(userid)
    if Cloud1:
        Cloud2 = await xowins(userid)
        return round((Cloud2/Cloud1)* 100)
    
    
    
#============================================this part is all about Show.xo_history===========================

def getname(*userid):
    Cursor.execute("select usernames from statuss where userid = %s or USERID = %s",(userid[0],userid[1]))
    Cloud = Cursor.fetchall()
    Cloud2 = []
    for num in Cloud:
        Cloud2.append(num[0])
    return Cloud2


def xowinnertimes(userid1,userid2):
    #userid1 = winner
    #userid2 = loser
    Cursor.execute("select much from xo_games where winner = %s and loser = %s",(userid1,userid2))
    Cloud = Cursor.fetchone()
    if not Cloud:
        Cloud = 0
    else:
        return Cloud[0]
    
    return Cloud

def xomoneywon(userid1,userid2):
    #userid1 = winner
    #userid2 = loser
    Cursor.execute("select wonmoney from xo_games where winner = %s and loser = %s",(userid1,userid2))
    Cloud = Cursor.fetchone()
    if not Cloud:
        Cloud = 0
    else:
        return Cloud[0]