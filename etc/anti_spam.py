import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
user_dict = dict()
banned_users = dict()

async def check_banned_users() -> None:
    current_time = time.time()
    for user, ban_time in banned_users.items():
        if current_time > ban_time:
            del banned_users[user]

async def reduce_user_scores(user_id: int) -> None:
    current_time = time.time()
    banned_users['userid'] = current_time + 10 * 60
    # TODO: need database

async def check_spam() -> None:
    for user, times in user_dict.items():
        if len(times) >= 5:
            if (times[5] - times[0]) <= 5:
                await reduce_user_scores(user_id)
        del user_dict[user]
    
async def add_user(user_id: int) -> None:
    if user_id in user_dict.keys():
        user_dict[user_id].append(time.time())
    else:
        user_dict[user_id] = [time.time()]



scheduler.add_job(check_spam, "interval", seconds=5)
scheduler.add_job(check_banned_users, "interval", minutes=5)

scheduler.start()