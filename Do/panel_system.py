from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions)
from pyrogram.enums import ChatMemberStatus
from db import CheckUserID, getlevel, give_score
from datetime import datetime, timedelta

from etc.Addition_and_subtraction import subtraction


# =============== command /mute ===================
# data[0]: function_call / data[1]: time_mute / data[2]: to_user_id / data[3]: user_id / data[4]: score_to_mute
async def create_keyboard(user_id: int, to_user_id: int):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('نیم ساعت - 50 امتیاز', callback_data=f'mute_confirm-30m-{to_user_id}-{user_id}-50'), ],
        [InlineKeyboardButton('2 ساعت - 100 امتیاز', callback_data=f'mute_confirm-2h-{to_user_id}-{user_id}-100'), ],
        [InlineKeyboardButton('4 ساعت - 300 امتیاز', callback_data=f'mute_confirm-4h-{to_user_id}-{user_id}-300'), ],
        [InlineKeyboardButton('8 ساعت - 600 امتیاز', callback_data=f'mute_confirm-8h-{to_user_id}-{user_id}-600'), ],
        [InlineKeyboardButton('12 ساعت - 1000 امتیاز', callback_data=f'mute_confirm-12h-{to_user_id}-{user_id}-1000'), ]
    ]
    )
    return keyboard


async def validate_to_user(user_id: int, to_user_id: int, client=None, message=None):
    is_reg = CheckUserID(to_user_id)
    # getlevel(to_user_id) to check user level

    user_level = getlevel(user_id)
    text = ''
    if not is_reg:
        text = 'یارو ثبت نام نکرده'

    elif getlevel(to_user_id) > user_level:
        text = 'لولش بیشتره'

    # check if to_user is admin or muted or doesnt exists on group
    elif client:
        to_user = await client.get_chat_member(message.chat.id, to_user_id)
        if to_user.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            text = 'ادمینه'
        elif to_user.status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED):
            text = 'در گروه حضور ندارد'
        else:
            try:
                if not to_user.permissions.can_send_messages:
                    text = 'میوت شده قبلا'
            except:
                pass

    if text:
        return text
    return True


async def mute_command(client, message, text):
    if message.reply_to_message:
        if not message.reply_to_message.from_user.is_bot and not message.reply_to_message.from_user.id == message.from_user.id:
            user_id = message.from_user.id
            to_user_id = message.reply_to_message.from_user.id
            user_score = give_score(user_id)
            validate = await validate_to_user(user_id, to_user_id, client, message)
            if validate is True:
                keybaord = await create_keyboard(user_id, to_user_id)
                await message.reply(
                    f'your score: {user_score}\nانتخاب کن چقدر میخوای ({message.reply_to_message.from_user.first_name}) میوت کنی',
                    reply_markup=keybaord)
            else:
                await message.reply(validate)
        else:
            await message.reply('درست ریپ بزن')
    else:
        await message.reply('رو یکی ریپلی بزن کص پدر')


# =============== confirm mute user ===================

async def confirm_mute_user(client, callback_query, data):
    user_id = int(data[3])
    score = int(data[4])

    if user_id == callback_query.from_user.id:
        user_score = give_score(user_id)
        if user_score >= score:
            time = data[1]
            data[0] = 'mute_user'
            confirm_data = '-'.join(data)
            data[0] = 'back_mute'
            back_data = '-'.join(data)
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('تایید', callback_data=confirm_data), ],
                [InlineKeyboardButton('برگشت', callback_data=back_data), ],
            ]
            )
            await callback_query.edit_message_text(f'برای تایید ({time}) با {score} امتیاز تایید کنید',
                                                   reply_markup=keyboard)
        else:
            await callback_query.answer('امتیاز کافی نداری', show_alert=True)
    else:
        await callback_query.answer('برو بازیتو کن بچه', show_alert=True)


# =============== back method ===================

async def back_method(client, callback_query, data):
    user_id = int(data[3])
    if user_id == callback_query.from_user.id:
        user_score = give_score(user_id)
        to_user_id = int(data[2])
        to_user_firstname = await client.get_users(to_user_id)
        to_user_firstname = to_user_firstname.first_name

        keybaord = await create_keyboard(user_id, to_user_id)
        await callback_query.edit_message_text(
            f'your score: {user_score}\nانتخاب کن چقدر میخوای ({to_user_firstname}) میوت کنی',
            reply_markup=keybaord)


# =============== mute user ===================

async def mute_user(client, callback_query, data):
    user_id = int(data[3])

    if user_id == callback_query.from_user.id:
        score = int(data[4])
        to_user_id = int(data[2])
        time = int(data[1][:-1])
        time_mute = timedelta(hours=time) if data[1][-1] == 'h' else timedelta(minutes=time)

        validate = await validate_to_user(user_id, to_user_id, client, callback_query.message)
        if validate is True:
            await client.restrict_chat_member(callback_query.message.chat.id, to_user_id, ChatPermissions(),
                                              datetime.now() + time_mute)

            to_user_firstname = await client.get_users(to_user_id)
            # check if user has enough score
            user_score = give_score(user_id)
            if user_score >= score:
                await subtraction(user_id, score)
                to_user_firstname = to_user_firstname.first_name
                await callback_query.edit_message_text(f'دویت عزیزمون {to_user_firstname} به مدت {data[1]} میوت شد و '
                                                       f'ازت {score} امتیاز کم کردم')
            else:
                await callback_query.answer('امتیاز کافی نداری', show_alert=True)
        else:
            await callback_query.answer(validate, show_alert=True)
    else:
        await callback_query.answer('برو بازیتو کن بچه', show_alert=True)
