from db import getname,xowinnertimes,xomoneywon
from datetime import datetime


async def xo_history(Client,Message,text):
    infomessage = await Client.send_message(Message.from_user.id,"|درحال جمع آوری اطلاعات . . .|")
    text2 = text[1].split("-")
    user_1 = text2[1]
    user_2 = text2[2]
    user_1_name = getname(user_1)
    user_2_name = getname(user_2)

    user1w = xowinnertimes(user_1,user_2)
    user2w = xowinnertimes(user_2,user_1)

    if user1w and user2w:
        winrate1 = round(user1w/user2w,2)
        winrate2 = round(user2w/user1w,2)
    else:
        if user1w:
            winrate1 = user1w
            winrate2 = 0
            user2w = "هیچ وقت"
        else:
            winrate1 = 0
            winrate2 = user2w
            user1w = "هیچ وقت"
    user1money = xomoneywon(user_1,user_2)
    user2money = xomoneywon(user_2,user_1)
    if user1money and user2money:
        moneyzarib1 = user1money/user2money
        moneyzarib2 = user2money/user1money
    else:
        if user1money:
            moneyzarib1 = user1money
            moneyzarib2 = 0
        else:
            moneyzarib1 = 0
            moneyzarib2 = user2money
            
    pl1point = winrate1*0.8 + moneyzarib1
    pl2point = winrate2*0.8 + moneyzarib2
    seconttext = ""
    if pl1point > pl2point:
        seconttext = f"🧮 | با در نظر گرفتن فاکتور ها از نظر کلی پلیر {user_1_name} عملکرد بهتری نسبت به {user_2_name} از خودش نشون داده 🥳"
    elif pl1point < pl2point:
        seconttext = f"🧮 | با در نظر گرفتن فاکتور ها از نظر کلی پلیر {user_2_name} عملکرد بهتری نسبت به {user_1_name} از خودش نشون داده 🥳"
    else:
        seconttext = "🧮 | با در نظر گرفتن فاکتور ها از نظر کلی هر دو پلیر دقیقا در یک سطح قرار دارند 🥳"
        
    await infomessage.edit_text(f"""📊 | تاریخچه بازی های {user_1_name} در مقابل {user_2_name} به این صورته ⤺

🎮 | تعداد برد های ({user_1_name}) تا کنون: {user1w}

🎮 | تعداد برد های ({user_2_name}) تا کنون: {user2w}

📈 | ضریب برد {user_1_name} مقابل {user_2_name} برابر با: [{winrate1}]


📈 | ضریب برد {user_2_name} مقابل {user_1_name} برابر با:  [{winrate2}]

——————————————————————————————

💰 | مقدار امتیاز کسب شده توسط {user_1_name} برابر : {user1money} امتیاز

💰 | مقدار امتیاز کسب شده توسط {user_2_name} برابر : {user2money} امتیاز


{seconttext}

T̷h̷i̷s r̷e̷p̷o̷r̷t i̷s o̷n̷l̷y v̷a̷l̷i̷d u̷n̷t̷i̷l  {datetime.now()}""")
    
    