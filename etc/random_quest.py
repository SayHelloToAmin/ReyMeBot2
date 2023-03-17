from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)
import random

task_math = dict()
task_click = dict()

# ================== quests ========================


async def quest_one(client):
    num_one = random.randint(1, 200)
    num_two = random.randint(1, 200)
    math = random.choice(['+', '-', '*'])
    answer = eval(f'{num_one}{math}{num_two}')
    score = random.randint(500, 2000)
    task_math[answer] = score

    text = '''پاسخ محاسبه ({num_one} {math} {num_two}) رو بفرستین تا ({score}) امتیاز برنده شید 😇
به عنوان مثال : جواب 5'''
    await client.send_message(-1001406922641, text)


async def quest_two(client):
    score = random.randint(500, 2000)
    task_id = random.randint(500, 2000)
    task_click[task_id] = score
    text = f'برای برنده شدن امتیاز({score}) دکمه زیرو بزن 😇'
    keybaord = InlineKeyboardMarkup([
        [InlineKeyboardButton('Touch Me', callback_data=f'click-{task_id}'),]]
        )
    await client.send_message(-1001406922641, text, reply_markup=keybaord)


# ================== check asnwers ========================

async def check_click_quest(client, callback_query, data):
    if data[1] in task_click:
        pass
        # TODO: need database

async def check_math_quest(client, message, text):
    if text[1] in task_math:
        pass
        # TODO: need database

# ================ task runner =========================-

async def start_random_task(client):
    which_task = random.choice(quest_one, quest_two)
    await which_task(client)


    
# in main ==================
# @app.on_callback_query()
# async def check_quest_answer(client, callback_query):
#     data = callback_query.data.split('-')
#     commands = {
#         'click': check_click_quest,
#     }
#     try:
#         await commands[data[0]](client, callback_query, data)
#     except:
#         pass