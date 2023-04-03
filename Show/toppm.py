from db import gettoppm


maintext = """⬳ ترتیب کاربران ربات بر اساس تعداد پیام ⤺

"""







num = 0


async def TopPm(Client,Message,text):
    order = gettoppm()
    global num,maintext
    for Cloud in order:
        num += 1
        if num == 1:
            maintext += f"""【 ♛ {Cloud[0]} with {Cloud[1]} pm !
"""
        elif num == 2:
            maintext += f"""【 ♚ {Cloud[0]} with {Cloud[1]} !
"""
        else:
            maintext += f"""【 {num}  -  ♙ {Cloud[0]} with {Cloud[1]}
"""
        if num <= 8:
            maintext += """┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
            """
            
    await Message.reply(maintext)
    maintext = """⬳ ترتیب کاربران ربات بر اساس تعداد پیام ⤺

"""