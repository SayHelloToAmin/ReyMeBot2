from pyrogram import Client, filters
from pyrogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                            InlineKeyboardButton)
from db import give_score , recxo
from etc.Addition_and_subtraction import subtraction, addiction

import random
import asyncio
import time
from typing import Union, List


xo_game = dict()
xo_spam = dict()
xo_price = dict()


async def create_xo_board(board: list, game_id: int, player_1, player_2):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text=columon,
                              callback_data=f'xo-{game_id}-{player_1}-{player_2}-{index_row}-{index_columon}') for
         index_columon, columon in enumerate(row)] for index_row, row in enumerate(board)
    ])
    return reply_markup


async def create_winner_board(board: list, win_coordinate: list):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='🟡' if (index_row, index_columon) in win_coordinate else columon,
                              callback_data='None') for index_columon, columon in enumerate(row)] for index_row, row in
        enumerate(board)
    ])
    return reply_markup


async def create_verify_xo_keyboard(score: int, user_id: int, user_first_name: str):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='شروع بازی', callback_data=f'xo_start-{score}-{user_id}-{user_first_name.strip("-")}')]
    ])
    return reply_markup


async def xo_verify(client: Client, message: Message, text):
    try:
        score = int(text[1])
    except Exception as e:
        pass
        score = False
    if score:
        user_id = message.from_user.id
        user_score = give_score(user_id)
        if user_score > score:
            user_first_name = message.from_user.first_name
            markup = await create_verify_xo_keyboard(score, user_id, user_first_name)
            await client.send_message(message.chat.id,
                                      f"بازیکن {user_first_name} درخواست شروع یک دوز داده برای شرکت در بازی و "
                                      f"گذاشتن {score} امتیاز وسط رو دکمه زیر کلیک کنید", reply_markup=markup)

        else:
            await message.reply(f'امتیاز کافی ندارید. امتیاز شما: {user_score}')
    else:
        await message.reply('عدد صحیح وارد کنید')

async def reduce_scores(score, user_id, user_first_name, to_user_name, to_user_id) -> Union[str, bool]:
    to_user_score = give_score(to_user_id)
    user_score = give_score(user_id)
    text_error = str()
    if to_user_score < score:
        text_error = f'{to_user_name} امتیاز کافی نداره'
        return text_error
    elif user_score < score:
        text_error = f'{user_first_name} امتیاز کافی نداره'
        return text_error
    await subtraction(to_user_id, score)
    await subtraction(user_id, score)
    return True


async def xo_send(_, callback_query: CallbackQuery, data):
    if callback_query.from_user.id != int(data[2]):
        score = int(data[1])
        to_user_score = give_score(callback_query.from_user.id)
        if to_user_score >= score:
            game_id = await callback_query.edit_message_text('درحال اماده سازی بازی')
            game_id = game_id.id
            board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                     [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
            player_1_id = int(data[2])
            player_1_name = data[3]
            player_2 = callback_query.from_user
            text = f'Player 1 Choose 🔴 {player_1_name}'

            # Final Validation To Check Players Score And If Passed Reduce Their Scores
            is_passed = await reduce_scores(score, player_1_id, player_1_name, player_2.first_name, player_2.id)
            if type(is_passed) == str:
                text = is_passed

            now = time.time()
            xo_game[game_id] = [player_1_id, board, player_1_name, player_2.first_name, now]
            xo_spam[game_id] = True
            xo_price[game_id] = [score, player_1_id, player_2.id]
            reply_markup = await create_xo_board(xo_game[game_id][1], game_id, player_1_id, player_2.id)
            await asyncio.sleep(1.2)
            await callback_query.edit_message_text(text=text,
                                                   reply_markup=reply_markup)

        else:
            await callback_query.answer('امتیاز کافی نداری', show_alert=True)
    else:
        await callback_query.answer('با خودت میخوای بازی کنی؟', show_alert=True)


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


async def check_winner(board, player_emoji, row, col) -> Union[list, bool]:
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

    return False


async def delete_game(game_id: int) -> None:
    del xo_game[game_id]
    del xo_spam[game_id]
    del xo_price[game_id]


async def edit_xo(client, callback_query, data):
    global xo_game
    await asyncio.sleep(random.uniform(0.300, 0.500))

    int_data = list(map(int, data[1:6]))  # Turn needed CallBacks to Int
    game_id: int = int_data[0]
    game: list = xo_game[game_id]
    turn: int = int(game[0])
    board: list = game[1]
    row: int = int_data[3]
    columon: int = int_data[4]
    player_1: int = int_data[1]
    player_2: int = int_data[2]
    player_1_name: str = game[2]
    player_2_name: str = game[3]
    turn_emoji: str = '🔴' if player_1 == turn else '🔵'
    next_turn_emoji = '🔵' if player_1 == turn else '🔴'
    if callback_query.from_user.id in (player_2, player_1):
        if turn == callback_query.from_user.id:
            if xo_spam[game_id]:
                xo_spam[game_id] = False
                if board[row][columon] == ' ':
                    board[row][columon] = turn_emoji
                    winner = await check_winner(board, turn_emoji, row, columon)
                    if winner:
                        reply_markup = await create_winner_board(board, winner)
                        winner_user = await client.get_users(turn)
                        win_price = xo_price[game_id][0]*2
                        await callback_query.edit_message_text(
                            f"بازیکن {winner_user.first_name} {turn_emoji} برنده {win_price} امتیاز شد 🎉",
                            reply_markup=reply_markup)
                        await addiction(winner_user.id, win_price)
                        if callback_query.from_user.id == player_1:
                            recxo(player_1,player_2,win_price)
                        else:
                            recxo(player_2,player_1,win_price)
                        await delete_game(game_id)
                        print('deleted')
                    else:
                        reply_markup = await create_xo_board(board, game_id, player_1, player_2)
                        next_turn_name = player_2_name if player_1 == turn else player_1_name
                        await callback_query.edit_message_text(
                            f"1 - ({player_1_name}) 🔴\n2 - ({player_2_name}) 🔵\n\n**نوبت:** {next_turn_name} {next_turn_emoji}",
                            reply_markup=reply_markup)
                        next_turn = player_2 if turn == player_1 else player_1
                        now = time.time()
                        xo_game[game_id] = [next_turn, board, player_1_name, player_2_name, now]
                    xo_spam[game_id] = True
                else:
                    await callback_query.answer('این دکمه از قبل انتخاب شده', show_alert=True)
            else:
                await callback_query.answer('اسپم نکن دوست گرامی', show_alert=True)
        else:
            await callback_query.answer('نوبتت نیست گل', show_alert=True)

    else:
        await callback_query.answer('برو دنبال درسو مشقت', show_alert=True)


async def is_game_equal(board: list) -> bool:
    empty_place = 0
    for row in board:
        empty_place += row.count(' ')
    if empty_place <= 42:
        return True
    return False


# TODO: Check Simultaneuos Attend For (xo_send) Function
# TODO: Check If Game Message Is Deleted Dont Count As Afk
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
            if not is_equal:
                await addiction(winner.id, price[0] * 2)
                await client.send_message(-1001452929879,
                                          f"بازیکن {afk_player.first_name} به دلیل بازی نکردن بعد از 2 دقیقه باخت و {price[0]} امتیاز به {winner.first_name} رسید ")
            await client.delete_messages(-1001452929879, gid)
            await delete_game(gid)