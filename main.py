from pyrogram import Client, filters

from Show.starts import *

from etc.Count import Counter1

from etc.anti_spam import *

from Show.showscore import score_shower
from Show.mylevel import mylevel
from etc.random_quest import *
from db import CheckUserID
from etc.run_all_tasks import scheduler

# Pyrogram Config : 

app = Client(
    'Reyme',
    api_id=6703845,
    api_hash="3eac821a6d1e0b0e2969ae0ad2f970ea",
    bot_token="1949862634:AAHlTHP-tNqz_DKK72aThdcIc48jlosg46M"
)


# =====================================================================

# custom filter to check if user in not registered
# async def check_reg_status(_, client, message):
#     text = message.text.split()[0].lower()
#     if text == "/start" or text == "/start@reymebot":
#         return True
#     else:
#         if CheckUserID(message.from_user.id):
#             return True
#         else:
#             await client.send_message(message.chat.id, 'ثبت نام نکردی')
#             return False

# async def check_reg_status_temp(client, message):
#     text = message.text.split()[0].lower()
#     if text == "/start" or text == "/start@reymebot":
#         return True
#     else:
#         if CheckUserID(message.from_user.id):
#             return True
#         else:
#             await client.send_message(message.chat.id, 'ثبت نام نکردی')
#             return False

# check_register = filters.create(check_reg_status)


# custom filter to check if user is banned
async def check_banned_user(_, __, message):
    if message.from_user.id in banned_users.keys():
        return False
    return True


spam_filter = filters.create(check_banned_user)


@app.on_message(filters.group & ~filters.channel & ~filters.bot & filters.text & spam_filter)
async def group_message(client, message):
    await Counter1(message)
    await add_user(message.from_user.id)
    text = message.text.split()
    commands = {
        "/start": first_start,
        "/start@reymebot": first_start,
        'جواب': check_math_quest,
        "/myscore": score_shower,
        "/myscore@reymebot": score_shower,
        "/mylevel": mylevel,
        "/mylevel@reymebot": mylevel

    }
    try:
        await commands[text[0].lower()](client, message, text)
    except Exception as e:
        print(e)



# private on message
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




# For random quests which need buttons
@app.on_callback_query(spam_filter )
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
scheduler.add_job(start_random_task, "interval", minutes=30, args=[app])
scheduler.add_job(check_spam, "interval", seconds=5, args=[app])
app.run()
