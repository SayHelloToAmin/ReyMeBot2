import db

import traceback
from etc import reporter

# =============Subtraction==============

async def subtraction(user_id: int, value: int):
    try:
        Cloud = db.givecount(user_id)
        if Cloud - value < 0:
            db.setscore(user_id, 0)
        else:
            db.setscore(user_id, Cloud - value)
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name)

# ===============Addiction=====================

async def addiction(user_id: int, value: int):
    try:
        Cloud = db.givecount(user_id)
        db.setscore(user_id, Cloud + value)
    except Exception as e:
        tb = e.__traceback__
        reporter.exceptf(tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name)