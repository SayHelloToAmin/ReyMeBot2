from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time


text_1 = 'page 1 text'
text_2 = 'page 2 text'

async def check_group_send(client, message, text):
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="𝚃𝚊𝚔𝚎 𝙼𝚎 𝚃𝚘 𝙿𝚟", url="https://t.me/reymebot?start=help")]])

    await message.reply('|— این کامند در گروه پشتیبانی نمیشود!', reply_markup=markup)


# check if 12 hours passed from button
async def check_help_expire(inline_date) -> bool:
    now = time.time()
    elapsed_time = now - inline_date
    elapsed_hours = elapsed_time / 3600
    if elapsed_hours > 12:
        return True
    return False

# create keybaord for page and close
async def create_keyboard(date, page):
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=('1✅' if page == '1' else '1'), callback_data=f'help-1-{date}')
                , InlineKeyboardButton(text=('2✅' if page == '2' else '2'), callback_data=f'help-2-{date}')
             ],
            [InlineKeyboardButton(text='close', callback_data=f'help-close-{date}')]
        ]
    )
    return markup

# ** /help command **
async def send_help(client, message, text):
    now = time.time()
    markup = await create_keyboard(now, '1')
    await message.reply(text_1, reply_markup=markup)

# ======================================

# if close button pressed change text and remove buttons
async def change_to_closed(callback_query):
    await callback_query.edit_message_text('Closed')


# if page button pressed change text
async def change_help_text(text, callback_query, button_date, page):
    markup = await create_keyboard(button_date, page)
    await callback_query.edit_message_text(text, reply_markup=markup)

# ** inline button clicked **
async def help_page(client, callback_query, data):
    button_date = float(data[2])
    is_expired = await check_help_expire(button_date)
    if not is_expired:
        if data[1] == '1':
            await change_help_text(text_1, callback_query, button_date, '1')
        elif data[1] == '2':
            await change_help_text(text_2, callback_query, button_date, '2')
        else:
            await change_to_closed(callback_query)

    else:
        await callback_query.answer('Expired send /help again', show_alert=True)
        await callback_query.message.delete()
