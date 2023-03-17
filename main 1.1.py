from pyrogram import client , filters
from mysql.connector import connection
import asyncio


# Pyrogram Config : 

app = client(
    'Reyme',
    api_id=6703845,
    api_hash="3eac821a6d1e0b0e2969ae0ad2f970ea",
    bot_token="1812849282:AAGZBXBy97vlj_z5gqu9ENxsl1qa8qCd6v4"
)
#=====================================================================

#Connect to MySQL Server : 
Db = connection.MySQLConnection(
    host = '127.0.0.1',
    user = "root",
    password = "KhodeAmin",
    database = "reymebot"


)

Cursor = Db.cursor() #=========> Thats What We Need In All Of DataBase's Requests

#======================================================================


@app.on_message(filters.private | filters.command('start'))
async def PrivateMessages(Clinet,Update):
    pass


