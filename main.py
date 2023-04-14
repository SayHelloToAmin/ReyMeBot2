from pyrogram import Client, filters
from Show.muted_and_by import ShowMutedBy, ShowMuted
from Show.starts import *
from etc.randomly import *
from etc.Count import Counter1
from etc.randomly import addpm, isthattime
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
from Show.toppm import TopPm
from Show.help import *
from etc.xo import *
from Show.xo_history import xo_history
import re
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

# all of group commands


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
    "/mute": mute_command,
    "/lstatus": lstatus,
    "/lstatus@reymebot": lstatus,
    "/buyxp": xpbuy,
    "/buyxp@reymebot": xpbuy,
    "/help": check_group_send,
    "/help@reymebot": check_group_send,
    "/mutedby": ShowMutedBy,
    "/mutedby@reymebot": ShowMutedBy,
    "/muted": ShowMuted,
    "/muted@reymebot": ShowMuted,
    "/toppm" : TopPm,
    "/toppm@reymebot" : TopPm,
    '/xo': xo_verify,

}

english_regex = re.compile(r'^[a-zA-Z0-9\s]+$')
@app.on_message(filters.group & ~filters.channel & ~filters.bot & filters.text & spam_filter)
async def group_message(client, message):
    global english_regex , current_question,commands
    
    await caller(message)
    
    if CheckUserID(message.from_user.id):
        if not isthattime:
            await Counter1(message)

    

    # from etc.Chatgpt import current_question
    # try:
    #     if message.reply_to_message.id == current_question.id:
    #         if CheckUserID(message.from_user.id):
    #             if english_regex.match(message.text):
    #                 await answer_handler(client,message)
    #             else:
    #                 await message.reply("ᴘʟᴇᴀꜱᴇ ᴜꜱᴇ ᴇɴɢʟɪꜱʜ ꜰᴏɴᴛ ᴏɴʟʏ!")
    #         else:
    #             reg_text = f"""😱| [{message.from_user.first_name}](tg://user?id={message.from_user.id}) چاقال 
    #                                         تو هنوز تو بات ثبت نشدی ! استارتش کون دیگه"""
    #             await message.reply(reg_text)
    # except:
    #     pass

    text = message.text.split()



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


privatecom = {
    "/help": send_help,
    "/help@reymebot": send_help

}

privatecom2 = {
    "help": send_help,
    "xo_his" : xo_history

}


# private on message

@app.on_message(filters.private)
async def private_message(client, message):
    global privatecom, privatecom2
    text = message.text.lower().split()
    if text[0] == "/start" or text[0] == "/start@reymebot":
        if len(text) == 1:
            await second_start(client, message)
        else:
            if CheckUserID(message.from_user.id):
                text2 = text[1].split("-")
                # all of start ==> commands will be here
                # -----------------------------------------------------------------------------------------------------
                if text2[0] in privatecom2:
                    await privatecom2[text2[0]](client, message, text)

            # --------------------------------------------------------------------------------------------------------
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
        'mute_user': mute_user,
        'help': help_page,
        'xo_start': xo_send,
        'xo': edit_xo,
        'xo_cancel': cancel_xo_request,
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
scheduler.add_job(start_random_task, "interval", minutes=19, args=[app])
scheduler.add_job(check_spam, "interval", seconds=7, args=[app])
scheduler.add_job(addpm, "interval", minutes=25, args=[app])
# scheduler.add_job(send_question, "interval", minutes=30, args=[app, -1001452929879])
scheduler.add_job(check_afk_xo, "interval", minutes=2, args=[app])
app.run()
