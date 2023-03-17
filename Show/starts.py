import db
import asyncio


# Handle /start in group (it doesn't do anything just show error to send it in pv again)

async def first_start(Client,Message,Text):
    if db.CheckUserID(Message.from_user.id):
        await Message.reply(f"جناپ [{Message.from_user.first_name}](tg://user?id={Message.from_user.id}) عزیز شما همین الانشم تو ربات ثبت شدین 😱")
    else:
        await Message.reply(f"😍عزیز برای ثبت اکانتت باید رباتو استارت کنی [{Message.from_user.first_name}](tg://user?id={Message.from_user.id})")



# Handle /start In Bot Pv (Register User Or Not If he is already registered)

async def second_start(Client,Message,Text):
    print(Message.from_user.id)
    if db.CheckUserID(Message.from_user.id):
        await Client.send_message(chat_id=Message.from_user.id,text=f"جناپ [{Message.from_user.first_name}](tg://user?id={Message.from_user.id}) عزیز شما همین الانشم تو ربات ثبت شدین 😱")
    else:
        Cloud = db.registeruser(Message.from_user.first_name,Message.from_user.id)
        if Cloud:
            await Client.send_message(chat_id=Message.from_user.id,text="😱دوست قشنگ و زیبام ثبتت کردم")
        else:
            await Client.send_message(chat_id=Message.from_user.id,text="Something Went Wrong . . . ")


