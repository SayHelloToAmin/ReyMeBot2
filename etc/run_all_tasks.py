from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .anti_spam import check_spam, check_banned_users
from .random_quest import start_random_task
scheduler = AsyncIOScheduler()

# anti spam
scheduler.add_job(check_spam, "interval", seconds=5)
scheduler.add_job(check_banned_users, "interval", minutes=5)
scheduler.add_job(check_banned_users, "interval", minutes=5)

scheduler.start()