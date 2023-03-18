import db
import asyncio
import main



def exceptf(file_name, function_name , userid):
    db.error_reporter(userid , f"An error occurred in {file_name} at {function_name} function")














#ino ok koooon

def report(Client , cursor , db):
    db.connect()
    cursor.excuse("SELECT max(id) FROM error")
    Cloud = cursor.fetchone()
    if Cloud[0] >= 5:
        Client.send_message(chat_id=908641353,text=f"{Cloud[0]} error has been recorded.")
        Client.send_message(chat_id=383456888,text=f"{Cloud[0]} error has been recorded.")
    else:
        pass
