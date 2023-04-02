from pyrogram import Client, filters

from Show.starts import *
from etc.randomly import *
from etc.Count import Counter1
from etc.randomly import addpm, pm, isthattime
from etc.anti_spam import *
from Do.buyxp import xpbuy
from Show.showscore import score_shower
from Show.mylevel import mylevel
from etc.random_quest import *
from db import *
from etc.run_all_tasks import scheduler
from etc.lottery2 import first
from Do.levelup import lvlup
from Do.pay import *
from Do.add_admin import *
from Do.panel_system import *
from Show.lotterystatus import lstatus

# Pyrogram Config : 

app = Client(
    'Reyme',
    api_id=6703845,
    api_hash="3eac821a6d1e0b0e2969ae0ad2f970ea",
    bot_token="1949862634:AAGWQyOS_0xKzD8FT1f1Ky3Gb9geoTmtByY"
)


# custom filter to check if user is banned
async def check_banned_user(_, __, message):
    if message.from_user.id in banned_users.keys():
        return False
    return True


spam_filter = filters.create(check_banned_user)


@app.on_message(filters.group & ~filters.channel & ~filters.bot & filters.text & spam_filter)
async def group_message(client, message):
    await caller(message)
    if CheckUserID(message.from_user.id):
        if not isthattime:
            await Counter1(message)
    text = message.text.split()
    commands = {
        "/start": first_start,
        "/start@reymebot": first_start,
        'جواب': check_math_quest,
        "/myscore": score_shower,
        "/myscore@reymebot": score_shower,
        "/mylevel": mylevel,
        "/mylevel@reymebot": mylevel,
        "/levelup": lvlup,
        "/levelup@reymebot": lvlup,
        "/lottery": first,
        "/lottery@reymebot": first,
        '/pay': pay_command,
        '/admin': add_admin,
        '/mute@reymebot': mute_command,
        "/lstatus" : lstatus,
        "/lstatus@reymebot" : lstatus,
        "/buyxp": xpbuy,
        "/buyxp@reymebot" : xpbuy

    }
    try:
        is_reg = CheckUserID(message.from_user.id)
        if (text[0].lower() in commands.keys()) and not is_reg:
            reg_text = f"""😱| [{message.from_user.first_name}](tg://user?id={message.from_user.id}) چاقال 
                                        تو هنوز تو بات ثبت نشدی ! استارتش کون دیگه"""
            await message.reply(reg_text)
        else:
            await add_user(message.from_user.id)
            await commands[text[0].lower()](client, message, text)
    except Exception as e:
        print(e)


# private on message
@app.on_message(filters.private)
async def private_message(client, message):
    print(text)
    text = message.text.split()
    commands = {
        "/start": second_start,
        "/start@reymebot": second_start
    }
    try:
        await commands[text[0].lower()](client, message, text)
    except:
        pass


# For random quests which need buttons
@app.on_callback_query(spam_filter)
async def check_quest_answer(client, callback_query):
    data = callback_query.data.split('-')
    commands = {
        'click': check_click_quest,
        'mute_confirm': confirm_mute_user,
        'back_mute': back_method,
        'mute_user': mute_user
    }
    try:
        is_reg = CheckUserID(callback_query.from_user.id)
        if data[0] in commands.keys() and not is_reg:
            reg_text = f"""😱| {callback_query.from_user.first_name} چاقال 
                                                   تو هنوز تو بات ثبت نشدی ! استارتش کون دیگه"""
            await callback_query.answer(reg_text, show_alert=True)
        else:
            await commands[data[0]](client, callback_query, data)
    except Exception as e:
        print(e)


# temp
# quests
scheduler.add_job(start_random_task, "interval", minutes=15, args=[app])
scheduler.add_job(check_spam, "interval", seconds=7, args=[app])
scheduler.add_job(addpm, "interval", minutes=25, args=[app])
app.run()
