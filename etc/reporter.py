
import asyncio




def exceptf(file_name, function_name , userid):
    error_reporter(userid , f"An error occurred in {file_name} at {function_name} function")














#ino ok koooon

async def report(client,cursor):
    cursor.execuse("SELECT max(id) FROM error")
    Cloud = Cursor.fetchone()
    if Cloud[0] >= 5:
        await client.send_message(chat_id=908641353,text=f"{Cloud[0]} error has been recorded.")
        await client.send_message(chat_id=383456888,text=f"{Cloud[0]} error has been recorded.")
    else:
        pass
