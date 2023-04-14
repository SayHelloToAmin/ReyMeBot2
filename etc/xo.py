from pyrogram import Client, filters
from pyrogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                            InlineKeyboardButton)
from pyrogram.errors import FloodWait

from db import give_score, recxo, xo_winrate, xocount, xogames, upname
from etc.Addition_and_subtraction import subtraction, addiction

import random
import asyncio
import time
from typing import Union, List

xo_game = dict()
xo_spam = dict()
xo_price = dict()
xo_expire = dict()


async def verify_expire(date) -> bool:
    now = time.time() - 300
    if now > date:
        return False
    return True


async def create_xo_board(board: list, game_id: int, player_1, player_2):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text=columon,
                              callback_data=f'xo-{game_id}-{player_1}-{player_2}-{index_row}-{index_columon}') for
         index_columon, columon in enumerate(row)] for index_row, row in enumerate(board)
    ])
    return reply_markup


async def create_winner_board(board: list, win_coordinate: list, pl1, pl2):
    inline_buttons = [[InlineKeyboardButton(text='🟡' if (index_row, index_columon) in win_coordinate else columon,
                                            callback_data='None') for index_columon, columon in enumerate(row)] for
                      index_row, row in
                      enumerate(board)]
    inline_buttons.append([InlineKeyboardButton(text='𝑴𝒐𝒓𝒆 𝑰𝒏𝒇𝒐𝒓𝒎𝒂𝒕𝒊𝒐𝒏',
                                                url=f'https://t.me/reymebot?start=xo_his-{pl1}-{pl2}')])
    reply_markup = InlineKeyboardMarkup(
        inline_buttons
    )
    return reply_markup


async def create_verify_xo_keyboard(score: int, user_id: int, user_first_name: str, date: float):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='شروع بازی',
                              callback_data=f'xo_start-{score}-{user_id}-{date}')],
        [InlineKeyboardButton(text='لغو درخواست', callback_data=f'xo_cancel-{user_id}')]
    ])
    return reply_markup


async def is_game_max() -> bool:
    if len(xo_game) >= 8:
        return True
    return False


async def xo_verify(client: Client, message: Message, text):
    user_id = message.from_user.id
    user_score = give_score(user_id)
    upname(user_id, message.from_user.first_name)

    try:
        if text[1] == '*':
            score = user_score
        else:
            score = int(text[1])
            if score <= 0:
                score = "wrong"
    except Exception as e:
        score = False

    if not await is_game_max():
        if type(score) is int or type(score) is float:
            if user_score >= score:
                user_first_name = message.from_user.first_name
                markup = await create_verify_xo_keyboard(score, user_id, user_first_name, time.time())
                winr = await xo_winrate(user_id)
                games = await xogames(user_id)
                await client.send_message(message.chat.id,
                                          f"""🎮 | یک درخواست بازی با شرط {score} امتیاز توسط {user_first_name} ارسال شده است !
🧨 | توجه : این درخواست فقط 5 دقیقه از زمان ارسال اعتبار دارد ! 

    📊 | تعداد بازی های {user_first_name} تاکنون : {games} 
    📈 | درصد برد : %{winr}
    ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
    برای قبول درخواست و ورود به بازی کلیک کنید⤺""", reply_markup=markup)

            else:
                await message.reply(f'امتیاز کافی ندارید. امتیاز شما: {user_score}')
        elif score == "wrong":
            await message.reply("‼️ | لطفا از فرمت درست و اعداد طبیعی استفاده کنید !")
        else:
            await message.reply(f"""❕ | برای شروع بازی از این فرمت استفاده کنید ⤺ 
    Ex) /xo <تعداد امتیاز شرط>
    🔆 | نکته : میتونی از * برای شرط کل امتیاز هات به جای تعداد امتیاز شرط استفاده کنی ! امتیاز شما : {user_score} """)
    else:
        await message.reply('تعداد بازی ها به حد نصاب رسیده است')


async def cancel_xo_request(client: Client, callback_query: CallbackQuery, data: list):
    if callback_query.from_user.id == int(data[1]):
        await callback_query.message.delete()
    else:
        await callback_query.answer('🤝| تو نمیتونی این درخواست رو لغو کنی!', show_alert=True)


async def reduce_scores(score, user_id, user_first_name, to_user_name, to_user_id) -> Union[str, bool]:
    to_user_score = give_score(to_user_id)
    user_score = give_score(user_id)
    if to_user_score < score:
        return f'{to_user_name} امتیاز کافی نداره'
    elif user_score < score:
        return f'{user_first_name} امتیاز کافی نداره'
    await subtraction(to_user_id, score)
    await subtraction(user_id, score)
    return True


async def xo_send(client: Client, callback_query: CallbackQuery, data: list):
    if not await is_game_max():
        if await verify_expire(float(data[3])):
            if callback_query.from_user.id != int(data[2]):
                score = float(data[1])
                to_user_score = give_score(callback_query.from_user.id)

                if to_user_score >= score:
                    await callback_query.message.delete()
                    game_msg = await client.send_message(callback_query.message.chat.id,
                                                         "|درحال آماده سازی تیبل . . .|")
                    game_id = game_msg.id
                    if game_id not in xo_game.keys():
                        board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

                        player_1_id: int = int(data[2])
                        player_1_name = await client.get_users(player_1_id)
                        player_1_name = player_1_name.first_name

                        player_2 = callback_query.from_user
                        text = f'🥳 ¦ بازی شروع شد !\n📍 | اولین حرکت با {player_1_name} ⚪️ شروع میشه ! انتخاب کن ⤺'

                        # Final Validation To Check Players Score And If Passed Reduce Their Scores
                        is_passed = await reduce_scores(score, player_1_id, player_1_name, player_2.first_name,
                                                        player_2.id)
                        if type(is_passed) == str:
                            text = is_passed
                            await callback_query.answer(text=text, show_alert=True)
                            return False  # Exit Function If We Got Error

                        # Create Game In Dicts
                        now = time.time()
                        xo_game[game_id] = [player_1_id, board, player_1_name, player_2.first_name, now]
                        xo_spam[game_id] = True
                        xo_price[game_id] = [score, player_1_id, player_2.id]
                        reply_markup = await create_xo_board(xo_game[game_id][1], game_id, player_1_id, player_2.id)

                        await asyncio.sleep(2.3)
                        await game_msg.edit_text(text, reply_markup=reply_markup)

                    else:
                        await _.send_message(-1001452929879, xo_game.keys())
                        await callback_query.answer('این بازی در جریانه', show_alert=True)
                else:
                    await callback_query.answer('امتیاز کافی نداری', show_alert=True)
            else:
                await callback_query.answer('با خودت میخوای بازی کنی؟', show_alert=True)
        else:
            await callback_query.answer('این درخواست منقضی شده', show_alert=True)
    else:
        await callback_query.answer('تعداد بازی ها به حد نصاب رسیده', show_alert=True)


async def diagonal_left(board, player_emoji, row, col) -> Union[list, bool]:
    first_row = min(row, col)
    first_col = col - first_row
    last_row = min(len(board) - row - 1, len(board[0]) - col - 1)
    count = 0
    coordinate = list()
    for index, i in enumerate(range((row - first_row), (row + last_row + 1))):
        try:
            move = board[i][first_col + index]
            if move == player_emoji:
                count += 1
                coordinate.append((i, first_col + index))
                if count == 4:
                    return coordinate
            else:
                count = 0
        except IndexError:
            pass
    return False


async def diagonal_right(board, player_emoji, row, col) -> Union[list, bool]:
    # get the first diagonal index
    first_row = min(row, len(board[0]) - col - 1)
    first_col = col + first_row
    # get the last diagonal index
    last_row = min(len(board) - row - 1, col)

    coordinate = list()
    count = 0
    for index, i in enumerate(range((row - first_row), (row + last_row + 1))):
        try:
            move = board[i][first_col - index]
            if move == player_emoji:
                count += 1
                coordinate.append((i, first_col - index))
                if count == 4:
                    return coordinate
            else:
                count = 0
        except IndexError:
            pass
    return False


async def gold_row_win(board, player_emoji, row) -> Union[list, bool]:
    coordinate = list()
    count = 0
    for index, i in enumerate(board):
        if i == player_emoji:
            count += 1
            coordinate.append((row, index))
            if count == 4:
                return coordinate
        else:
            count = 0
            coordinate.clear()
    return False


async def gold_col_win(board, player_emoji, col) -> Union[list, bool]:
    coordinate = list()
    count = 0
    for index, i in enumerate(board):
        if i == player_emoji:
            count += 1
            coordinate.append((index, col))
            if count == 4:
                return coordinate
        else:
            count = 0
            coordinate.clear()
    return False


async def check_winner(board, player_emoji, row, col) -> Union[list, bool, str]:
    # Check Columons
    columons = [board[i][col] for i in range(7)]
    if columons.count(player_emoji) >= 4:
        is_win = await gold_col_win(columons, player_emoji, col)
        if is_win:
            return is_win

    # Check Row
    if board[row].count(player_emoji) >= 4:
        is_win = await gold_row_win(board[row], player_emoji, row)
        if is_win:
            return is_win

    # Check Diagonal
    winner = await diagonal_left(board, player_emoji, row, col)
    if winner:
        return winner

    winner = await diagonal_right(board, player_emoji, row, col)
    if winner:
        return winner

    # Check If Game Is Equal
    if await is_game_equal(board):
        return 'Equal'

    # If Nothing Happend Continue
    return False


async def delete_game(game_id: int) -> None:
    del xo_game[game_id]
    del xo_spam[game_id]
    del xo_price[game_id]


async def update_game_message(callback_query, player_1_name, player_2_name, next_turn_name, next_turn_emoji,
                              reply_markup, bet, userid1, userid2):
    pe1 = ""
    pe2 = ""
    if player_1_name == next_turn_name:
        pe1 = "🗡"
    else:
        pe2 = "🗡"

    await callback_query.edit_message_text(
        f"""
🕹 | [{player_1_name}](tg://user?id={userid1}) ⚪️ {pe1}
💰 | Bet : {bet}
🕹 | [{player_2_name}](tg://user?id={userid2}) ⚫️ {pe2}
- - - - - - - - - - - - - - - - - - - - - - - - -
حالا نوبت {next_turn_name} {next_turn_emoji} شد ! انتخاب کن <-فقط دو دقیقه وقت داری ⏱->  ⤺""",
        reply_markup=reply_markup)


async def edit_xo(client, callback_query: CallbackQuery, data):
    global xo_game, xo_price
    int_data = list(map(int, data[1:6]))  # Turn needed CallBacks to Int
    player_1: int = int_data[1]
    player_2: int = int_data[2]

    if callback_query.from_user.id in (player_2, player_1):
        await asyncio.sleep(random.uniform(0.700, 1.200))
        game_id: int = int_data[0]
        game: list = xo_game[game_id]
        turn: int = int(game[0])
        board: list = game[1]
        row: int = int_data[3]
        columon: int = int_data[4]
        player_1_name: str = game[2]
        player_2_name: str = game[3]
        turn_emoji: str = '⚪️' if player_1 == turn else '⚫'
        next_turn_emoji: str = '⚫️' if player_1 == turn else '⚪️'

        if turn == callback_query.from_user.id:
            if xo_spam[game_id]:
                if board[row][columon] == ' ':
                    xo_spam[game_id] = False
                    board[row][columon] = turn_emoji
                    winner = await check_winner(board, turn_emoji, row, columon)
                    if winner:
                        winner_user = await client.get_users(turn)
                        if type(winner) != str:
                            reply_markup = await create_winner_board(board, winner, player_1, player_2)
                            win_price = xo_price[game_id][0] * 2
                            await callback_query.edit_message_text(
                                f"""🎊 ¦ بازی تموم شد! 

🕹 | {player_1_name} ⚪️ 
💰 | Bet : {xo_price[game_id][0] * 2}
🕹 | {player_2_name} ⚫️ 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

🏆 | پلیر {winner_user.first_name} بازیو برد و {xo_price[game_id][0] * 2} امتیاز رو با خودش به خونه برد!""",
                                reply_markup=reply_markup)
                            await addiction(winner_user.id, win_price)
                            # TODO: Check
                            xocount(player_1, player_2)
                            if callback_query.from_user.id == player_1:
                                recxo(player_1, player_2, win_price)
                            else:
                                recxo(player_2, player_1, win_price)
                            print('deleted')

                        else:
                            reply_markup = await create_xo_board(board, game_id, player_1, player_2)
                            oponent = player_2 if turn == winner_user.id else player_1
                            await callback_query.edit_message_text(f"""🎊 ¦ بازی تموم شد! 

🕹 | {player_1_name} ⚪️ 
💰 | Bet : {xo_price[game_id][0] * 2}
🕹 | {player_2_name} ⚫️ 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

🙅🏿‍♂️ | به دلیل مساوی شدن هیچکس امتیاز نمیگیره !""", reply_markup=reply_markup)
                            xocount(player_1, player_2)
                            await addiction(winner_user.id, xo_price[game_id][0])
                            await addiction(oponent, xo_price[game_id][0])

                        await delete_game(game_id)
                    else:
                        reply_markup = await create_xo_board(board, game_id, player_1, player_2)
                        next_turn_name = player_2_name if player_1 == turn else player_1_name

                        # Check If Bot Get A FloodWait, Wait Until Its Over And Update Game
                        try:
                            await update_game_message(callback_query, player_1_name, player_2_name, next_turn_name,
                                                      next_turn_emoji, reply_markup, xo_price[game_id][0], player_1,
                                                      player_2)
                        except FloodWait as e:
                            await callback_query.answer(f"به دلیل اسپم لطفا {e.value + 2} ثانیه صبر کنید",
                                                        show_alert=True)
                            await asyncio.sleep(e.value + 2)
                            await update_game_message(callback_query, player_1_name, player_2_name, next_turn_name,
                                                      next_turn_emoji,
                                                      reply_markup, xo_price[game_id][0], player_1, player_2)

                        next_turn = player_2 if turn == player_1 else player_1
                        now = time.time()
                        xo_game[game_id] = [next_turn, board, player_1_name, player_2_name, now]
                    xo_spam[game_id] = True
                else:
                    await callback_query.answer("این خونه از قبل انتخاب شده", show_alert=True)
            else:
                await callback_query.answer('صبر کن تا درخواست قبلیت انجام شه ❕❗️', show_alert=True)
        else:
            await callback_query.answer('هنوز نوبت تو نشده ❕❗️', show_alert=True)

    else:
        await callback_query.answer('تو فقط یه تماشاچی ای ❕❗️', show_alert=True)


async def is_game_equal(board: list) -> bool:
    empty_place = 0
    for row in board:
        empty_place += row.count(' ')
    if empty_place == 0:
        return True
    return False


# TODO: Check Simultaneuos Attend For (xo_send) Function
# TODO: Check If Game Message Is Deleted Dont Count As Afk
# TODO: Send Game Again
async def check_afk_xo(client: Client) -> None:
    for gid, game in list(xo_game.items()):
        now = time.time() - 120
        previous = game[4]
        if now > previous:
            price = xo_price[gid]
            turn = game[0]
            afk_player = await client.get_users(turn)
            winner = price[2] if price[1] == turn else price[1]
            winner = await client.get_users(winner)
            is_equal = await is_game_equal(game[1])
            xocount(winner.id, afk_player.id)
            recxo(winner.id, afk_player.id, price[0] * 2)
            if not is_equal:
                await addiction(winner.id, price[0] * 2)

                await client.send_message(-1001406922641,
                                          f"💤 | متاسفانه بازیکن {afk_player.first_name} به دلیل AFK از بازی خارج و {price[0] * 2} امتیاز به {winner.first_name} رسید ! ")
            else:
                # Give Scores Back If Game Is Equal
                await addiction(winner.id, price[0])
                await addiction(afk_player.id, price[0])

            await client.delete_messages(-1001406922641, gid)
            await delete_game(gid)
