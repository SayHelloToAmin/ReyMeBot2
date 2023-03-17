from etc.db import *

async def start_test(client, message, text=None):
    Cursor.exceute()
    await message.reply('slm jende')