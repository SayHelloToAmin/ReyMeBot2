import time
from .Addition_and_subtraction import subtraction
from .check_registered_user import check_user_reg




user_dict = dict()
banned_users = dict()


# check banned user date to un ban them
# scheduler task
async def check_banned_users() -> None:
    current_time = time.time()
    for user, ban_time in list(banned_users.items()):
        if current_time > ban_time:
            del banned_users[user]


# if user recognized az spammer score will be reduced
async def reduce_user_scores(user_id: int) -> float:
    current_time = time.time()
    banned_users[user_id] = current_time + 300
    count_user_messages = len(user_dict[user_id])
    score_to_reduce = count_user_messages * 10
    await subtraction(user_id, score_to_reduce)
    return score_to_reduce


async def send_ban_message(client, user_id, reduced_score):
    user_info = await client.get_users(user_id)
    first_name = user_info.first_name
    text = f"🫂 | زنتو گاییدم ({first_name}) سر اسپمت بن میشی و {reduced_score} امتیاز ازت کسر میشه."
    await client.send_message(-1001406922641, text)

# check first on fifth message of user time to make sure is not spam
# scheduler task
async def check_spam(client) -> None:
    for user_id, times in list(user_dict.items()):
        if len(times) >= 5:
            try:
                if (times[-1] - times[-5]) <= 9:
                    reduced_score = await reduce_user_scores(user_id)
                    await send_ban_message(client, user_id, reduced_score)
            except IndexError:
                pass
        del user_dict[user_id]


# with every user text, message date will be saved
async def add_user(user_id: int) -> None:
    # is_reg = await check_user_reg(user_id)
    # if not is_reg:
    #     pass
    if user_id in user_dict.keys():
        user_dict[user_id].append(time.time())
    else:
        user_dict[user_id] = [time.time()]



