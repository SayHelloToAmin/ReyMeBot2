from pyrogram import Client , filters
import asyncio
import db
from Show.starts import *
import asyncio
# from etc.anti_spam import *

# Pyrogram Config : 

app = Client(
    'Reyme',
    api_id=6703845,
    api_hash="3eac821a6d1e0b0e2969ae0ad2f970ea",
    bot_token="1812849282:AAGZBXBy97vlj_z5gqu9ENxsl1qa8qCd6v4"
)
#=====================================================================


#======================================================================


@app.on_message(filters.private)
async def private_message(client , message):
    before_text = message.text.lower()
    text = before_text.split()
    commands = {
        "/start" : second_start,
        "/start@reymebot" : second_start
    }
    try:
        print("injaaaa")
        await commands[text[0].lower()](client, message, text)
    except:
        pass


@app.on_message(filters.group & ~filters.channel & ~filters.bot & filters.text)
async def group_message(client , message):
    before_text = message.text.lower()
    text = before_text.split()
    commands = {
        "/start" : first_start,
        "/start@reymebot" : first_start
        
    }
    try:
        await commands[text[0].lower()](client, message, text)
    except:
        pass





app.run()