from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton)
import random
from .Addition_and_subtraction import addiction

task_math = dict()
task_click = dict()


# ================== quests ========================


async def quest_math(client):
    num_one = random.randint(1, 200)
    num_two = random.randint(1, 200)
    math = random.choice(['+', '-', '*'])
    answer = eval(f'{num_one}{math}{num_two}')
    score = random.randint(50, 100)
    task_math[answer] = score

    text = f'''پاسخ محاسبه ({num_one} {math} {num_two}) رو بفرستین تا ({score}) امتیاز برنده شید 😇
به عنوان مثال : جواب 5'''
    await client.send_message(-1001406922641, text)


async def quest_click(client):
    score = random.randint(10, 30)
    task_id = random.randint(500, 2000)
    task_click[task_id] = score
    text = f'برای برنده شدن امتیاز({score}) دکمه زیرو بزن 😇'
    keybaord = InlineKeyboardMarkup([
        [InlineKeyboardButton('Touch Me', callback_data=f'click-{task_id}'), ]]
    )
    await client.send_message(-1001406922641, text, reply_markup=keybaord)


# ================== check asnwers ========================

async def check_click_quest(client, callback_query, data):
    if data[1] in task_click.keys():
        task_id = data[1]
        score = task_click[task_id]
        user_id = callback_query.from_user.id
        await addiction(user_id, score)
        del task_click[task_id]


async def check_math_quest(client, message, text):
    if text[1] in task_math.keys():
        answer = text[1]
        score = task_math[answer]
        user_id = message.from_user.id
        await addiction(user_id, score)
        del task_math[answer]


# ================ task runner =========================-

async def start_random_task(client):
    which_task = random.choice(quest_math, quest_click)
    await which_task(client)
