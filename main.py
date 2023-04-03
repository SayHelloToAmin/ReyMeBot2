from pyrogram import Client, filters
from Show.muted_and_by import ShowMutedBy , ShowMuted
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
from Show.help import CheckGroupSend , SendHelp
# Pyrogram Config : 


app = Client(
    'Reyme',
    api_id=6703845,
    api_hash="3eac821a6d1e0b0e2969ae0ad2f970ea",
    bot_token="1949862634:AAFwtwsp3P-Q32qyOs0XA1mGebEK6fLRzIs"
)

# custom filter to check if user is banned
async def check_banned_user(_, __, message):
    if message.from_user.id in banned_users.keys():
        return False
    return True


spam_filter = filters.create(check_banned_user)





#all of group commands


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
        "/mute":mute_command,
        "/lstatus" : lstatus,
        "/lstatus@reymebot" : lstatus,
        "/buyxp": xpbuy,
        "/buyxp@reymebot" : xpbuy,
        "/help" : CheckGroupSend,
        "/help@reymebot" : CheckGroupSend,
        "/mutedby" : ShowMutedBy,
        "/mutedby@reymebot":ShowMutedBy,
        "/muted" : ShowMuted,
        "/muted@reymebot":ShowMuted

    }







@app.on_message(filters.group & ~filters.channel & ~filters.bot & filters.text & spam_filter)
async def group_message(client, message):
    await caller(message)
    if CheckUserID(message.from_user.id):
        if not isthattime:
            await Counter1(message)
    text = message.text.split()
    global commands
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
        pass







privatecom = {
    "/help" : SendHelp,
    "/help@reymebot" : SendHelp
    
}


privatecom2 = {
    "help":SendHelp
    
    
    
    
    
}




# private on message

@app.on_message(filters.private)
async def private_message(client, message):
    global privatecom , privatecom2
    text = message.text.lower().split()
    if text[0] == "/start" or text[0] == "/start@reymebot":
        if len(text) == 1:
            await second_start(client,message)
        else:
            if CheckUserID(message.from_user.id):
                # all of start ==> commands will be here
                #-----------------------------------------------------------------------------------------------------
                if text[1] in privatecom2:
                    await privatecom2[text[1]](client, message, text)
                    
            #--------------------------------------------------------------------------------------------------------
            else:
                message.reply(f"""😱| [{message.from_user.first_name}](tg://user?id={message.from_user.id}) چاقال 
                                        تو هنوز تو بات ثبت نشدی ! استارتش کون دیگه""")
    else:
        is_reg = CheckUserID(message.from_user.id)
        if (text[0] in privatecom.keys()) and not is_reg:
            reg_text = f"""😱| [{message.from_user.first_name}](tg://user?id={message.from_user.id}) چاقال 
                                        تو هنوز تو بات ثبت نشدی ! استارتش کون دیگه"""
            await message.reply(reg_text)
        else:
            await add_user(message.from_user.id)
            await privatecom[text[0].lower()](client, message, text)

    




















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
        pass























# temp
# quests
scheduler.add_job(start_random_task, "interval", minutes=19, args=[app])
scheduler.add_job(check_spam, "interval", seconds=7, args=[app])
scheduler.add_job(addpm, "interval", minutes=25, args=[app])
app.run()
