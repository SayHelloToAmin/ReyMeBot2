from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton)
import random
from .Addition_and_subtraction import addiction

task_math = dict()
task_click = dict()


# ================== quests ========================


async def quest_math(client):
    task_math.clear()
    num_one = random.randint(1, 500)
    num_two = random.randint(1, 500)
    math = '-'
    answer = eval(f'{num_one}{math}{num_two}')
    score = random.randint(50, 100)
    task_math[str(answer)] = score
    print(answer)
    text = f'''پاسخ محاسبه ({num_two} {math} {num_one}) رو بفرستین تا ({score}) امتیاز برنده شید 😇
به عنوان مثال : جواب 5'''
    # salap : -1001406922641
    # test gap : -1001452929879
    await client.send_message(-1001452929879, text)


async def quest_click(client):
    task_click.clear()
    score = random.randint(10, 30)
    task_id = random.randint(500, 2000)
    task_click[str(task_id)] = score
    text = f'برای برنده شدن امتیاز({score}) دکمه زیرو بزن 😇'
    keybaord = InlineKeyboardMarkup([
        [InlineKeyboardButton('Touch Me', callback_data=f'click-{task_id}'), ]]
    )
    # salap : -1001406922641
    # test gap : -1001452929879
    await client.send_message(-1001452929879, text, reply_markup=keybaord)


# ================== check asnwers ========================

async def check_click_quest(client, callback_query, data):
    if data[1] in task_click.keys():
        task_id = data[1]
        score = task_click[task_id]
        user_id = callback_query.from_user.id
        await addiction(user_id, score)
        del task_click[task_id]
        first_name = callback_query.from_user.first_name
        await client.send_message(callback_query.message.chat.id,
                                  f"کاربر {first_name} شما برنده شدید و {score} امتیاز بردید")

async def check_math_quest(client, message, text):
    if text[1] in task_math.keys():
        answer = text[1]
        score = task_math[answer]
        user_id = message.from_user.id
        await addiction(user_id, score)
        del task_math[answer]
        first_name = message.from_user.first_name
        await client.send_message(message.chat.id,
                                  f"کاربر {first_name} شما درست جواب دادید و {score} امتیاز بردید")


# ================ task runner =========================-
# scheduler task
async def start_random_task(client):
    which_task = random.choice([quest_math, quest_click])
    await which_task(client)
