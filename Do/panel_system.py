from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions)
from pyrogram.enums import ChatMemberStatus
from db import CheckUserID, getlevel, give_score, muterecorder
from datetime import datetime, timedelta

from etc.Addition_and_subtraction import subtraction


# =============== command /mute ===================
# data[0]: function_call / data[1]: time_mute / data[2]: to_user_id / data[3]: user_id / data[4]: score_to_mute
async def create_keyboard(user_id: int, to_user_id: int):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('🤫⌛️| نیم ساعت : 450 امتیاز', callback_data=f'mute_confirm-30m-{to_user_id}-{user_id}-450'), ],
        [InlineKeyboardButton('🤫⌛️| یک ساعت : 800 امتیاز', callback_data=f'mute_confirm-1h-{to_user_id}-{user_id}-800'), ],
        [InlineKeyboardButton('🤫⌛️| دو ساعت : 1500 امتیاز', callback_data=f'mute_confirm-2h-{to_user_id}-{user_id}-1500'), ],
        [InlineKeyboardButton('🤫⌛️| شیش ساعت : 2800 امتیاز', callback_data=f'mute_confirm-6h-{to_user_id}-{user_id}-2800'), ],
        [InlineKeyboardButton('🤫⌛️| دوازده ساعت : 5000 امتیاز', callback_data=f'mute_confirm-12h-{to_user_id}-{user_id}-5000'), ]
    ]
    )
    return keyboard


async def validate_to_user(user_id: int, to_user_id: int, client=None, message=None):
    is_reg = CheckUserID(to_user_id)
    # getlevel(to_user_id) to check user level

    user_level = getlevel(user_id)
    text = ''
    if not is_reg:
        text = f"هنوز ثبت نام نکرده😱{message.reply_to_message.from_user.first_name} "

    elif getlevel(to_user_id) > user_level:
        text = '🫡 |کسی که میخوای میوتش کنی لولش از تو بالاتره !'

    # check if to_user is admin or muted or doesnt exists on group
    elif client:
        to_user = await client.get_chat_member(message.chat.id, to_user_id)
        if to_user.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            text = '🫡 |کسی که میخوای میوتش کنی ادمین گپه!'
        elif to_user.status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED):
            text = '🫡 |کسی که میخوای میوتش کنی اصلا تو گپ نیست!'
        else:
            try:
                if not to_user.permissions.can_send_messages:
                    text = '🫡 |کسی که میخوای میوتش کنی از قبل میوت شده!'
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
                    f'🤐 | انتخاب کن دقیقا چقدر میخوای {message.reply_to_message.from_user.first_name} میوت باشه ؟ امتیاز فعلیت : {user_score}',
                    reply_markup=keybaord)
            else:
                await message.reply(validate)
        else:
            await message.reply('💩 | رو یه یوزر حقیقی ریپلای بزن !')
    else:
        await message.reply('💩 | باید رو یکی ریپلای بزنی و از این کامند استفاده کنی!')


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
            await callback_query.edit_message_text(f'✅ | یک بار دیگه تایید کن {score} امتیاز برای {time} میوت !',
                                                   reply_markup=keyboard)
        else:
            await callback_query.answer('❌ | امتیاز کافی برای اینکار نداری!', show_alert=True)
    else:
        await callback_query.answer('🤡 | تورو کی ریده ؟', show_alert=True)


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
            f'🤐 | انتخاب کن دقیقا چقدر میخوای {to_user_firstname} میوت باشه ؟ امتیاز فعلیت : {user_score}',
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

            to_user_firstname = await client.get_users(to_user_id)
            # check if user has enough score
            user_score = give_score(user_id)
            if user_score >= score:
                # mute if gave any error send it to telegram
                try:
                    await client.restrict_chat_member(callback_query.message.chat.id, to_user_id, ChatPermissions(),
                                                      datetime.now() + time_mute)
                    await subtraction(user_id, score)
                    muterecorder(user_id, to_user_id)  # Log Mute Users
                except:
                    await client.send_message(-1001452929879, f'error user:{to_user_firstname}')

                to_user_firstname = to_user_firstname.first_name
                await callback_query.edit_message_text(f'🤐 | با موفقیت {to_user_firstname} رو میوت برای کردم و {score} امتیازم ازت کم کردم ! {data[1]} بعد انمیوت میشی 🐉')
            else:
                await callback_query.answer('❌ | امتیاز کافی برای اینکار نداری!', show_alert=True)
        else:
            await callback_query.answer(validate, show_alert=True)
    else:
        await callback_query.answer('🤡 | تورو کی ریده ؟', show_alert=True)
