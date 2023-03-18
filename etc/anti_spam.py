import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .Addition_and_subtraction import subtraction

scheduler = AsyncIOScheduler()
user_dict = dict()
banned_users = dict()


# check banned user date to un ban them
async def check_banned_users() -> None:
    current_time = time.time()
    for user, ban_time in banned_users.items():
        if current_time > ban_time:
            del banned_users[user]


# if user recognized az spammer score will be reduced
async def reduce_user_scores(user_id: int) -> None:
    current_time = time.time()
    banned_users[userid] = current_time + 10 * 60
    count_user_messages = len(user_dict[user_id])
    score_to_reduce = count_user_messages // 2
    await subtraction(user_id, score_to_reduce)


# check first on fifth message of user time to make sure is not spam
async def check_spam() -> None:
    for user, times in user_dict.items():
        if len(times) >= 5:
            if (times[5] - times[0]) <= 5:
                await reduce_user_scores(user_id)
        del user_dict[user]


# with every user text, message date will be saved
async def add_user(user_id: int) -> None:
    if user_id in user_dict.keys():
        user_dict[user_id].append(time.time())
    else:
        user_dict[user_id] = [time.time()]


scheduler.add_job(check_spam, "interval", seconds=5)
scheduler.add_job(check_banned_users, "interval", minutes=5)

scheduler.start()
