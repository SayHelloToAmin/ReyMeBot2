import db
import traceback


levelbar = {0:"══════════ 0%",1:"▰═════════ 10%",2:"▰▰════════ 20%",3:"▰▰▰═══════ 30%",4:"▰▰▰▰══════ 40%",5:"▰▰▰▰▰═════ 50%",
            6:"▰▰▰▰▰▰════ 60%",7:"▰▰▰▰▰▰▰═══ 70%",8:"▰▰▰▰▰▰▰▰══ 80%",9:"▰▰▰▰▰▰▰▰▰═ 90%",
            10:"▰▰▰▰▰▰▰▰▰▰ 100%"}

deftext1 = """⍡  [{firstname}](tg://user?id={ids}) چاقال 
【 لول فعلیت : {level}   ὣ
و فقط {menha} کصپی دیگه برا لول بعدیت نیاز داری⤸ 】

 {dic}  ∤  {xp} ／ {need}"""

deftext2 = """⍡  [{firstname}](tg://user?id={ids}) چاقال 
【 لول فعلیت : {level}   ὣ
 و همین الانم زیادی کصپی جمع کردی و میتونی بری لول بعد (/levelup) 】

 {dic}  ∤  {xp} ／ {need}"""

async def configure(userid):
    Cloud = db.getxp(userid)
    xp = Cloud[0]
    needed = Cloud[1]
    lvl = db.getlevel(userid)
    if Cloud[1] - Cloud[0] >= 0:
        percent = int(str(((xp / needed) * 100)/10).split(".")[0])
        return [True,xp , needed , percent , lvl]
    else:
        return [False , xp , needed , lvl]
            

        
        

async def mylevel(Client,Message,text):
    userid = Message.from_user.id
    name = Message.from_user.first_name
    if db.CheckUserID(userid):
        if Message.reply_to_message:
            if db.checkrank(userid):
                if db.CheckUserID(Message.reply_to_message.from_user.id):
                    Cloud = await configure(Message.reply_to_message.from_user.id)
                    if not Cloud[0]:
                        await Message.reply(f"سرورم این یارو لولش {Cloud[3]} و همین الانشم زیادی کصپی داره.")
                    else:
                        await Message.reply(f"سرورم این یارو لولش {Cloud[4]} تاس")
                else:
                    await Message.reply(f"😱|این  {Message.reply_to_message.from_user.first_name} چاقال هنوز ثبت نام نکرده ...")
            else:
                await Message.reply("بتوچه بچه کونی")
        else:
            Cloud2 = await configure(userid)
            Cloud3 = (Cloud2[2]-Cloud2[1])
            if Cloud2[0]:
                texxt = deftext1.format(level=Cloud2[4],menha=Cloud3,dic=levelbar[Cloud2[3]],xp=Cloud2[1],need=Cloud2[2],ids=userid,firstname=name)
                await Message.reply(texxt)
            else:
                await Message.reply(deftext2.format(level=Cloud2[3],dic=levelbar[10],xp=Cloud2[1],need=Cloud2[2],ids=userid,firstname=name))
    else:
        await Message.reply(f"""😱| [{name}](tg://user?id={userid}) چاقال 
                            تو هنوز تو بات ثبت نشدی ! استارتش کون دیگه""")