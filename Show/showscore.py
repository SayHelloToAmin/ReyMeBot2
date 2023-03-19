import db


import traceback
from etc import reporter


async def scoreshower(Client,Message,text):
    Cloud = Message.from_user.id
    Cloud2 = Message.reply_to_message.from_user.id
    if db.checkrank(Cloud):
        pass


