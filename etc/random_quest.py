from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton)
import random
from .Addition_and_subtraction import addiction
from .check_registered_user import check_user_reg


import traceback


task_math = dict()
task_click = dict()


# ================== quests ========================


async def quest_math(client):
    task_math.clear()
    num_one = random.randint(1, 500)
    num_two = random.randint(1, 500)
    math = '-'
    answer = str(eval(f'{num_one}{math}{num_two}'))
    score = random.randint(50, 100)
    task_math[answer] = [score]
    text = f'''پاسخ محاسبه ({num_two} {math} {num_one}) رو بفرستین تا {score} امتیاز برنده شید 😇
    به عنوان مثال : جواب 5'''
    # salap : -1001406922641
    # test gap : -1001452929879
    message = await client.send_message(-1001406922641, text)
    task_math[answer].append(message.id)


async def quest_click(client):
    task_click.clear()
    score = random.randint(10, 30)
    task_id = str(random.randint(500, 2000))
    task_click[task_id] = [score]
    text = f"👇🏿برای بردن ({score}) امتیاز بمالش👇🏻"
    keybaord = InlineKeyboardMarkup([
        [InlineKeyboardButton('Touch Me', callback_data=f'click-{task_id}'), ]]
    )
    # salap : -1001406922641
    # test gap : -1001452929879
    message = await client.send_message(-1001406922641, text, reply_markup=keybaord)
    task_click[task_id].append(message.id)

# ================== check asnwers ========================

async def check_click_quest(client, callback_query, data):
    # is_reg = await check_user_reg(callback_query.from_user.id)
    # if not is_reg:
    #     reg_text = f"😱| {callback_query.from_user.first_name} چاقال هنوز ثبت نام نکرده ..."
    #     await client.send_message(callback_query.message.chat.id, reg_text)
    if data[1] in task_click.keys():
        task_id = data[1]
        score = task_click[task_id][0]
        message_id = task_click[task_id][1]
        user_id = callback_query.from_user.id
        await addiction(user_id, score)
        del task_click[task_id]
        first_name = callback_query.from_user.first_name
        await client.delete_messages(callback_query.message.chat.id, message_id)
        await client.send_message(callback_query.message.chat.id,
                                  f"🤡🏆 ¦ خایمال {first_name} انگار زودتر از بقیه مالیدیش و {score} امتیاز گرفتی!")

async def check_math_quest(client, message, text):
    # is_reg = await check_user_reg(message.from_user.id)
    # if not is_reg:
    #     reg_text = f"😱| {message.from_user.first_name} چاقال هنوز ثبت نام نکرده ..."
    #     await client.send_message(message.chat.id, reg_text)
    if text[1] in task_math.keys():
        answer = text[1]
        score = task_math[answer][0]
        message_id = task_math[answer][1]
        user_id = message.from_user.id
        await addiction(user_id, score)
        del task_math[answer]
        first_name = message.from_user.first_name
        await client.delete_messages(message.chat.id, message_id)
        await message.reply(f"🧮🤡 ¦ ریاضیدان {first_name} "
                            f"تونستی درست دوتا عددو جمع و تفریق کنی و {score} امتیاز فرو کردم بهت.")


# ================ task runner =========================-
# scheduler task
async def start_random_task(client):
    which_task = random.choice([quest_math, quest_click])
    await which_task(client)
