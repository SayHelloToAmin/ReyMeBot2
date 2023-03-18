from pyrogram import Client, filters
import asyncio
import db
from Show.starts import *
import asyncio

from etc import Count
from etc.anti_spam import *
from etc.random_quest import *
from etc.run_all_tasks import scheduler
# Pyrogram Config : 

app = Client(
    'Reyme',
    api_id=6703845,
    api_hash="3eac821a6d1e0b0e2969ae0ad2f970ea",
    bot_token="1812849282:AAGZBXBy97vlj_z5gqu9ENxsl1qa8qCd6v4"
)


# =====================================================================


@app.on_message(filters.private)
async def private_message(client, message):
    text = message.text.split()
    commands = {
        "/start": second_start,
        "/start@reymebot": second_start
    }
    try:
        await commands[text[0].lower()](client, message, text)
    except:
        pass


# custom filter to check if user is banned
async def check_banned_user(_, __, message):
    if message.from_user.id in banned_users.keys():
        return False
    return True


spam_filter = filters.create(check_banned_user)


@app.on_message(filters.group & ~filters.channel & ~filters.bot & filters.text & spam_filter)
async def group_message(client, message):
    await Count.count(message)
    await add_user(message.from_user.id)

    text = message.text.split()
    commands = {
        "/start": first_start,
        "/start@reymebot": first_start,
        'جواب': check_math_quest,

    }
    try:
        await commands[text[0].lower()](client, message, text)
    except Exception as e:
        print(e)

# For random quests which need buttons
@app.on_callback_query(spam_filter)
async def check_quest_answer(client, callback_query):
    data = callback_query.data.split('-')
    commands = {
        'click': check_click_quest,
    }
    try:
        await commands[data[0]](client, callback_query, data)
    except Exception as e:
        print(e)


# temp
# quests
scheduler.add_job(start_random_task, "interval", minutes=60, args=[app])
app.run()
