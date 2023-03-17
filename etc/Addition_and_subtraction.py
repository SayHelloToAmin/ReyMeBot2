import db



#=============Subtraction==============

def Subtraction(user_id,value):
    Cloud = db.givecount(user_id)
    if Cloud - value < 0:
        db.setscore(user_id,0)
    else:
        db.setscore(user_id,Cloud - value)


#===============Addiction=====================

def addiction(user_id,value):
    Cloud = db.givecount(user_id)
    db.setscore(user_id,Cloud + value)