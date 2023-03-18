import db


# =============Subtraction==============

async def subtraction(user_id: int, value: int):
    Cloud = db.givecount(user_id)
    if Cloud - value < 0:
        db.setscore(user_id, 0)
    else:
        db.setscore(user_id, Cloud - value)


# ===============Addiction=====================

async def addiction(user_id: int, value: int):
    Cloud = db.givecount(user_id)
    db.setscore(user_id, Cloud + value)
