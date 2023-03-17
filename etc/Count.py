import db
import asyncio

#============Count Messages============


#this function will check if user are registered , count and add his chats.

async def count(Message):
    if db.CheckUserID(Message.from_user.id):
        db.counter(Message.from_user.id)
    else:
        pass
