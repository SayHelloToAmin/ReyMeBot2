
from db import lotterystatus , checkrank , CheckUserID


textt = """-وضعیت حساب لاتاری شما [{first}](tg://user?id={id}) به این شکل است :⤹

🎮 | کل بازی های انتخاب شده : {game} ≛

🎟 | تک عدد های حدس زده شده : {one} ≛

🎫 | جفت عدد های حدس زده شده : {two} ≛

🥉 | سه عدد های حدس زده شده : {three} ≛

🥈| چهار عدد های حدس زده شده : {four} ≛

🥇| و پنج عدد های درست حدس زده شده : {five} ≛

🎰 | جک پات ها : {jack} ≛"""

async def lstatus(Client,Message,text):
    global textt
    userid = Message.from_user.id
    if Message.reply_to_message:
        if checkrank(userid):
            if CheckUserID(Message.reply_to_message.from_user.id):
                status = await lotterystatus(Message.reply_to_message.from_user.id)
                await Message.reply(textt.format(first=Message.reply_to_message.from_user.first_name,id=Message.reply_to_message.from_user.id,game=status[0],one=status[1],two=status[2],three=status[3],four=status[4],five=status[5],jack=status[6]))
            else:
                await Message.reply(f"😱| {Message.reply_to_message.from_user.first_name} چاقال هنوز ثبت نام نکرده ...")
        else:
            await Message.reply("Access Denied ! ")
    else:
        status = await lotterystatus(Message.from_user.id)
        await Message.reply(textt.format(first=Message.from_user.first_name,id=Message.from_user.id,game=status[0],one=status[1],two=status[2],three=status[3],four=status[4],five=status[5],jack=status[6]))
