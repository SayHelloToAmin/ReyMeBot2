import db
import traceback
from etc import reporter

# =============Subtraction==============

async def subtraction(user_id: int, value: float):
    Cloud = db.give_score(user_id)
    if Cloud - value < 0:
        db.setscore(user_id, 0)
    else:
        db.setscore(user_id, Cloud - value)


# ===============Addiction=====================

async def addiction(user_id: int, value: int):
    Cloud = db.give_score(user_id)
    db.setscore(user_id, Cloud + value)
