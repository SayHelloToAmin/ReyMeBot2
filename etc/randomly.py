import db
import random
import asyncio
from etc.Addition_and_subtraction import subtraction
pm = 0
isthattime = False

async def caller(Message):
    global isthattime , pm
    pm += 1
    if isthattime:
        test = Message.from_user.id
        if db.CheckUserID(test):
            test = Message.from_user.id
            await Message.reply("🤡 | چت ؟ -55 امتیاز!")
            await subtraction(test,55.0)





async def addpm(Client):
    global pm , isthattime
    if pm >= 110:
        pm = 0
        isthattime = True
        wtime = random.randint(90,150)
        await Client.send_message(-1001406922641,f"""👹👹 | از همین لحظه پنالتی تایم شروع شد !
          تا {wtime} ثانیه دیگه هر پیام (جز گیف و استیکر) = کسر 55 امتیاز シ""")
        await asyncio.sleep(wtime)
        isthattime = False
        pm = 0
        await Client.send_message(-1001452929879,"⏱⏱ | پنالتی تایم از الان تموم شد ! میتونید چت کنید .シ")
    else:
        pm = 0

