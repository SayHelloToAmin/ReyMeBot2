from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton





async def CheckGroupSend(Client,Message,Text):
    markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="𝚃𝚊𝚔𝚎 𝙼𝚎 𝚃𝚘 𝙿𝚟",url="https://t.me/reymebot?start=help")]])
    
    await Message.reply('|— این کامند در گروه پشتیبانی نمیشود!', reply_markup=markup)
    
    
    
async def SendHelp(Client,Message,Text):
    await Message.reply("test message")