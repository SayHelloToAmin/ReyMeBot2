from db import give_score, CheckUserID
from etc.Addition_and_subtraction import addiction, subtraction


async def pay_command(client, message, text):
    is_safe = True
    user_id = message.from_user.id
    user_score = give_score(user_id)
    # ============== Validations ====================

    # check if the score is not int break the function
    try:
        entered_score = float(text[1])
        if entered_score < 0:
            raise ValueError
    except:
        await message.reply('『 لطفا یک عدد حسابی انتخاب کنید 』')
        return None

    # check if user didnt reply break the function
    try:
        to_user_id = message.reply_to_message.from_user.id
    except:
        await message.reply('『  رو یکی ریپلای کن  』')
        return None
    # check if to_user is registered
    is_to_user_reg = CheckUserID(to_user_id)
    if not is_to_user_reg:
        await message.reply(f"هنوز ثبت نام نکرده😱{message.reply_to_message.from_user.first_name} ")

    # check if entered_score is more than user score
    elif entered_score > user_score:
        await message.reply('『  بیشتر از داراییت میخوای ببخشی ؟  』')

    # check if user_score has less than 50 score give error
    elif user_score <= 50 or (user_score-entered_score) <= 50:
        await message.reply('『  حداقل 50 امتیاز باید تو اکانتت بمونه  』')

    elif entered_score == 0:
        await message.reply('『  احتمالا نمیتونم 0 امتیاز انتقال بدم  』')

    elif message.from_user.id == to_user_id:
        await message.reply('『  به خودت ؟؟؟  』')
    # if every thing was fine take and give socres
    elif is_safe:
        first_name = message.reply_to_message.from_user.first_name
        await subtraction(user_id, entered_score)
        await addiction(to_user_id, entered_score)
        await message.reply(f"🥳 | خب {entered_score} ازت کم کردم و به {first_name} اضافه کردم .")
