import time
from .Addition_and_subtraction import subtraction


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
async def reduce_user_scores(user_id: int) -> None:
    current_time = time.time()
    print()
    banned_users[user_id] = current_time + 10 * 60
    count_user_messages = len(user_dict[user_id])
    score_to_reduce = count_user_messages // 2
    await subtraction(user_id, score_to_reduce)


# check first on fifth message of user time to make sure is not spam
# scheduler task
async def check_spam() -> None:
    print(user_dict)
    for user_id, times in list(user_dict.items()):
        if len(times) >= 5:
            if (times[5] - times[0]) <= 5:
                await reduce_user_scores(user_id)
        del user_dict[user_id]


# with every user text, message date will be saved
async def add_user(user_id: int) -> None:
    if user_id in user_dict.keys():
        user_dict[user_id].append(time.time())
    else:
        user_dict[user_id] = [time.time()]



