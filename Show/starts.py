import db
import asyncio


# Handle /start in group (it doesn't do anything just show error to send it in pv again)

async def FIrst_STart(Client,Message,Text):
    if db.CheckUserID(Message.from_user.id):
        tag = f'[{Message.from_user.first_name}](tg://user?id={Message.from_user.id})'
        await Message.reply(f"جناپ {tag} عزیز شما همین الانشم تو ربات ثبت شدین 😱")
    else:
        await Message.reply(f"{tag} 😍عزیز برای ثبت اکانتت باید رباتو استارت کنی ")
