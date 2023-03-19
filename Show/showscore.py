import db


import traceback
from etc import reporter


async def scoreshower(Client,Message,text):
    Cloud = Message.from_user.id
    Cloud2 = None
    if Message.reply_to_message :
        Cloud2 = Message.reply_to_message.from_user.id
    else:
        pass
    if db.checkrank(Cloud):
        if Cloud2 != None:
            if db.CheckUserID(Cloud2):
                Cloud3 = db.give_score(Cloud2)
                await Message.reply(f"""{Message.reply_to_message.from_user.first_name} 
                درحال حاضر {Cloud3} امتیاز داره 🤡""")
            else:
                await Message.reply(f"هنوز ثبت نام نکرده😱{Message.reply_to_message.from_user.first_name} ")
        else:
            Cloud3 = db.give_score(Cloud)
            await Message.reply(f"دوست خوب و مهربونم در حال حاضر {Cloud3} امتیاز داری 😱")
    else:
        Cloud3 = db.give_score(Cloud)
        await Message.reply(f"دوست خوب و مهربونم در حال حاضر {Cloud3} امتیاز داری 😱")