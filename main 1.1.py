from pyrogram import Client , filters
import asyncio
import db
from Show.starts import *
from etc.anti_spam import *

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
    text = message.text.split()
    commands = {

    }
    try:
        await commands[text[0].lower()](client, message, text)
    except:
        pass


@app.on_message(filters.group & ~filters.channel & ~filters.bot)
async def group_message(client , message):
    text = message.text.split()
    commands = {

    }
    try:
        await commands[text[0].lower()](client, message, text)
    except:
        pass





app.run()