import db

import traceback



async def score_shower(Client, Message, text):
    Cloud = Message.from_user.id
    Cloud2 = None
    # check register
    if db.CheckUserID(Cloud):
        # check mikone message reply ya sade
        if Message.reply_to_message:
            Cloud2 = Message.reply_to_message.from_user.id
        else:
            pass
        # check mikone admin ino ferestade ya na
        if db.checkrank(Cloud):
            # check mikone reply bood ya na
            if Cloud2 != None:
                if db.CheckUserID(Cloud2):
                    Cloud3 = db.give_score(Cloud2)
                    await Message.reply(f"""{Message.reply_to_message.from_user.first_name} 
                    درحال حاضر {Cloud3} امتیاز داره 🤡""")
                else:
                    await Message.reply(f"😱|این  {Message.reply_to_message.from_user.first_name} چاقال هنوز ثبت نام نکرده ...")
            else:
                Cloud3 = db.give_score(Cloud)
                await Message.reply(f" پدسگ در حال حاضر {Cloud3} امتیاز داری 😱")
        else:
            Cloud3 = db.give_score(Cloud)
            await Message.reply(f" پدسگ در حال حاضر {Cloud3} امتیاز داری 😱")
    else:
        await Message.reply(f"|پدرسگ هنوز ثبت نام نکردی|")
