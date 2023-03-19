import db
import asyncio
import traceback
from etc import reporter

#============Count Messages============


#this function will check if user are registered , count and add his chats.

async def Shomarande(Message):
    try:
        if db.CheckUserID(Message.from_user.id):
            db.counter(Message.from_user.id)
        else:
            pass
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name , Message.from_user.id)
