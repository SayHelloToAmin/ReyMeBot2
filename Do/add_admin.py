from db import checkrank
from pyrogram.errors import BadRequest

async def add_admin(client, message, text=None):
    is_admin = checkrank(message.from_user.id)
    if is_admin:
        if message.reply_to_message:
            try:
                await client.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                await message.reply('ادمین شد')
            except BadRequest:
                await message.reply('Something Went Wrong...')

        else:
            await message.reply('ریپلی کن')
