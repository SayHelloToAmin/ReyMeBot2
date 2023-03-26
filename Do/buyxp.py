from db import getlevel,getxp,give_score,upxp
from etc.Addition_and_subtraction import *
async def xpbuy(Client,Message,text):
    userid = Message.from_user.id
    lvl = getlevel(userid)
    score = give_score(userid)
    xpn = getxp(userid)
    first_name = Message.from_user.first_name
    if len(text) != 2:
        if (xpn[1]-xpn[0]) > 0:
            await Message.reply(f"""😇 | برای خرید کصپی باید به این صورت دستور رو وارد کنی : ⤹
— /buyxp (مقدار کصپی)
📝 | ضمنا هر امتیاز به اندازه 2 کصپی ارزش داره و شما {xpn[1]-xpn[0]} کصپی برای ورود به لول {lvl+1} نیاز دارید و درحال حاضر {score} امتیاز دارید !""")
        else:
            await Message.reply(f"""⍡  [{first_name}](tg://user?id={userid}) چاقال 
【 لول فعلیت : {lvl}   ὣ
 و همین الانم زیادی کصپی جمع کردی و میتونی بری لول بعد (/levelup) 】""")
    else:
        xpbuy=0
        try:
            xpbuy = int(text[1])
            if xpbuy <= 0:
                raise ValueError
        except:
            await Message.reply("🥀 | لطفا یه عدد طبیعی با فرمت درست وارد کن .")
        else:
            if score >= (xpbuy/2):
                try:
                    await subtraction(userid,xpbuy/2)
                except:
                    await Message.reply("Something went wrong...")
                else:
                    try:
                        upxp(userid,xpn[0]+xpbuy)
                    except:
                        await addiction(userid,int(xpbuy/2))
                        await Message.reply("something went wrong... try later")
                    else:
                        await Message.reply(f"✅ | تبریک! [{first_name}](tg://user?id={userid}) خرید {xpbuy} کصپی انجام شد و {xpbuy/2} امتیاز ازت کم کردم .")
            else:
                await Message.reply("❌ | امتیاز کافی برای اینکار نداری!")