from db import CheckUserID , mutedby , muted



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
                await Message.reply("""⬳ این بنده خدا تا حالا میوتت نکرده 🧌
𝒢𝒪𝒪𝒟 𝐹𝑅𝐼𝐸𝒩𝒟𝒮""")
            
        else:
            await Message.reply(f"😱|این  {Message.reply_to_message.from_user.first_name} چاقال هنوز ثبت نام نکرده ...")
    else:
        await Message.reply("⬳ دقیقا باید سابقه کیو ببینم ؟ ریپلای کن دیگه 🧌")
            

async def ShowMuted(Client,Message,text):
    if Message.reply_to_message:
        if CheckUserID(Message.reply_to_message.from_user.id):
            userid1 = Message.from_user.id
            userid2 = Message.reply_to_message.from_user.id
            Cloud = muted(userid1,userid2)
            if Cloud:
                await Message.reply(f"""⬳ بنظر میرسه [{Message.reply_to_message.from_user.first_name}](tg://user?id={userid2}) رو تا حالا {Cloud[0]} بار میوت کردی 🧌
— و تاریخ آخرین میوتش توسط تو ⤺
⌦ {Cloud[1]}""")
            else:
                await Message.reply("""⬳ تا حالا میوتش نکردی ! 🧌 
𝒢𝒪𝒪𝒟 𝐹𝑅𝐼𝐸𝒩𝒟𝒮""")
            
        else:
            await Message.reply(f"😱|این  {Message.reply_to_message.from_user.first_name} چاقال هنوز ثبت نام نکرده ...")
    else:
        await Message.reply("⬳ دقیقا باید سابقه کیو ببینم ؟ ریپلای کن دیگه 🧌")
            