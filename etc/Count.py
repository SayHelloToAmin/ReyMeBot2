import db
import asyncio

#============Count Messages============
global hi 
hi = 1
#this function will check if user are registered , count and add his chats.

async def count(Client,Message,Text):
    if db.CheckUserID(Message.from_user.id):
        db.counter()
