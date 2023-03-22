from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions)
from db import CheckUserID, getlevel, give_score
from datetime import datetime, timedelta


# =============== command /mute ===================
async def create_keyboard(user_id: int, to_user_id: int):
    keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('نیم ساعت - 50 امتیاز', callback_data=f'mute-30m-{to_user_id}-{user_id}'), ],
            [InlineKeyboardButton('2 ساعت - 100 امتیاز', callback_data=f'mute-2h-{to_user_id}-{user_id}'), ],
            [InlineKeyboardButton('4 ساعت - 300 امتیاز', callback_data=f'mute-4h-{to_user_id}-{user_id}'), ],
            [InlineKeyboardButton('8 ساعت - 600 امتیاز', callback_data=f'mute-5h-{to_user_id}-{user_id}'), ],
            [InlineKeyboardButton('12 ساعت - 1000 امتیاز', callback_data=f'mute-6h-{to_user_id}-{user_id}'), ]
        ]
    )
    return keyboard

async def validate_to_user(user_id: int, to_user_id: int):
    is_reg = CheckUserID(to_user_id)
    to_user_level = getlevel(to_user_id)

    user_level = getlevel(user_id)
    text = str()

    if not is_reg:
        text += 'یارو ثبت نام نکرده'
        return text
    elif to_user_level > user_level:
        text += 'لولش بیشتره'
        return text
    return True

async def mute_command(client, message, text):
    if message.reply_to_message:
        if not message.reply_to_message.from_user.is_bot:
            user_id = message.from_user.id
            to_user_id = message.reply_to_message.from_user.id
            user_score = give_score(user_id)
            validate = await validate_to_user(user_id, to_user_id)
            if validate is True:
                keybaord = await create_keyboard(user_id, to_user_id)
                await message.reply(f'your score: {user_score}\nانتخاب کن چقدر میخوای ({message.reply_to_message.from_user.first_name}) میوت کنی', reply_markup=keybaord)
            else:
                await message.reply(validate)
        else:
            await message.reply('باتو میخوای میوت کنی')
    else:
        await message.reply('رو یکی ریپلی بزن کص پدر')

# =============== mute user ===================

async def mute_user(client, callback_query, data):
    user_id = int(data[3])
    to_user_id = int(data[2])
    time = data[1][:-1]
    time_mute = timedelta(hours=time) if data[1][-1] == 'h' else timedelta(minutes=time)
    # time_mute = time_mute_checker[:-1]
    # print(user_id, callback_query.from_user.id)
    if user_id == callback_query.from_user.id:
        validate = await validate_to_user(user_id, to_user_id)
        if validate is True:
            await app.restrict_chat_member(message.chat.id, to_user_id, ChatPermissions(),
                                           datetime.now() + time_mute)
            await callback_query.answer('mute shod')
        else:
            await callback_query.answer(validate)
    else:
        await callback_query.answer('برو بازیتو کن بچه')