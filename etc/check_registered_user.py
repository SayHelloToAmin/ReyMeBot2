from db import CheckUserID

async def check_user_reg(user_id, client=None, message=None):
    is_registered = CheckUserID(user_id)
    if is_registered:
        return True
    return False

