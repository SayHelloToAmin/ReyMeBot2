from db import CheckUserID , mutedby



async def ShowMutedBy(Client,Message,text):
    if Message.reply_to_message:
        if CheckUserID(Message.reply_to_message.from_user.id):
            userid1 = Message.from_user.id
            userid2 = Message.reply_to_message.from_user.id
            Cloud = mutedby(userid1,userid2)
            if Cloud:
                await Message.reply(f"""| بنظر میرسه [{Message.reply_to_message.from_user.first_name}](tg://user?id={userid2}) تا به حال {Cloud[0]} بار میوتت کرده 🧌
— و تاریخ آخرین میوتت توسط ایشون ⤺
⌦ {Cloud[1]}""")
            else:
                await Message.reply("⬳ این بنده خدا تا حالا میوتت نکرده 🧌")
            
        else:
            await Message.reply(f"😱|این  {Message.reply_to_message.from_user.first_name} چاقال هنوز ثبت نام نکرده ...")