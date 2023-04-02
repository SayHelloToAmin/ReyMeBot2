import db
from etc.randomly import isthattime


# ============Count Messages============


# this function will check if user are registered , count and add his chats.

async def Counter1(Message):
    if db.CheckUserID(Message.from_user.id):
        db.counter(Message.from_user.id)
    else:
        pass    

