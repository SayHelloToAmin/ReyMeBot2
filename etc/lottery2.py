import time
import asyncio
import random
from etc.Addition_and_subtraction import subtraction
from db import lotterysetter , upname
# set up variables for the lottery
participants = {}
lottery_numbers = []
lottery_started = False
last_lottery = 0
lottext = """🐉 | لاتاری تموم شد ! نتایج به این صورته : ⤥ 
 """
winners = {}
nameid = {}
wnameid = {}



async def run_lottery(Client,Message):
    await Client.send_message(Message.chat.id,"⏱ |  فرصت ارسال تموم شد ! در حال بررسی جواب ها ! 🔥")
    global participants, lottery_numbers, lottery_started , last_lottery , lottext,winners , nameid , wnameid
    lottery_numbers = random.sample(range(0, 100), 6)
    for username, user_numbers in participants.items():
        correct_guesses = len(set(user_numbers) & set(lottery_numbers))
        if correct_guesses == 0:
            lottext = lottext + f"""
            ❌ | دوست خوبمون {username} نتونست هیچ کدوم از عدد هارو حدس بزنه ... """    
        elif correct_guesses >= 1 and correct_guesses <= 5:
                point = (correct_guesses * 80) + (len(participants)*40)
                winners[username] = str(correct_guesses)+"-"+str(point)
                wnameid[username] = nameid[username]
                lottext = lottext + f"""
🏆 | دوست خوبمون {username} تونست {correct_guesses} از عدد هارو درست حدس بزنه ... + {point}"""
        else:
            point = 1400 + (len(participants)*40)
            winners[username] = str(correct_guesses)+"-"+str(point)
            wnameid[username] = nameid[username]
            lottext = lottext + f"""
            🎰🎉  |⬱ جک پات ⇶  دوست سفیدمون {username} تونست همه عدد هارو درست حدس بزنه ... + {point} 🏆"""
    lottext = lottext + f"""

📝 | اعداد صحیح باری : {lottery_numbers}
🤞🏿 |  20 دقیقه دیگه دوباره میتونین با /lottery یه لاتاری دیگه رو شروع کنین"""
    await lotterysetter(winners,wnameid)
    winners.clear()
    await Client.send_message(Message.chat.id,lottext)
    last_lottery = time.time()
    lottery_started = False
    participants.clear()
    lottery_numbers = []
    nameid.clear()
    wnameid.clear()
    

    #     # reset participant's guesses
    #     participants[username] = []
    # lottery_started = False







async def startlot(Client,Message,text):
    global participants, lottery_numbers, lottery_started , last_lottery
    await Message.reply("""🥳 | لاتاری با موفقیت شروع شد !!! از بین 0 تا 40 باید 6 عدد رو حدس بزنید و بفرستید ! 
⏳| حواستون باشه فقط 20 دقیقه فرصت دارین عدد های خودتونو بفرستین !


💵 | ورودی هر نفر 40 امتیاز و جایزه کسی که هر 6 عدد رو درست حدس بزنه 1400 امتیاز هست ! 
【 به هر حال به کسانی که حتی یک عدد رو درست حدس زدن جایزه داده میشود و به ازای هر شرکت کننده به جایزه ها 40 پوینت اضافه میشود 】
⍡ برای ارسال اعداد خود میتوانید از این مثال استفاده کنید 

Ex) /lottery 1 2 3 4 5 6""")
    lottery_started = True
    await asyncio.sleep(600)
    await Client.send_message(Message.chat.id, f"""⏳ | فقط 10 دقیقه دیگه تا اعلام نتایج باقی مونده ! 
Ex) /lottery 1 2 3 4 5 6""")
    await asyncio.sleep(300)
    await Client.send_message(Message.chat.id, f"""⏳ | فقط 5 دقیقه دیگه تا اعلام نتایج باقی مونده ! 
Ex) /lottery 1 2 3 4 5 6""")
    await asyncio.sleep(240)
    await Client.send_message(Message.chat.id, f"""⏳ | فقط 1 دقیقه دیگه تا اعلام نتایج باقی مونده ! 
Ex) /lottery 1 2 3 4 5 6""")
    if len(participants) != 0:
        await run_lottery(Client,Message)
    else:
        await Client.send_message(Message.chat.id,"🥀 | متاسفانه لاتاری شرکت کننده ای نداشت ... درشو بستیم .")
        lottery_started = False
        participants.clear()
        last_lottery = time.time()-600
        nameid.clear()
    


async def first(Client,Message,text):
    upname(Message.from_user.id,Message.from_user.first_name)
    global participants, lottery_numbers, lottery_started , last_lottery , nameid , wnameid
    if len(text) == 1:
        if lottery_started:
            await Message.reply("""❤️‍🔥 | لاتاری همین الانشم شروع شده ! تا وقت داری عدد هاتو بده ⤺
⥭  Ex) /lottery 1 2 3 4 5 6""")
        else:
            now = time.time()
            if (now - last_lottery) >= 1200:
                await startlot(Client,Message,text)
            else:
                await Message.reply(f"""🫠 | متاسفانه فعلا نمیتونم لاتاری بعدیو استارت کنم !
                  تا لاتاری بعدی ⥆ {round((1200-(now-last_lottery))/60)} min  ☫ """)
    else:
        if lottery_started:
            try:
                user_numbers = list(map(int, Message.text.split()[1:]))
                if len(user_numbers) != 6 :
                    raise ValueError("❗️ | شما باید دقیقا 6 عدد را از بین 0 تا 40 انتخاب کنید !")
                for num in user_numbers:
                    if num < 0 or num > 40:
                        raise ValueError("❗️ | شما باید عداد را از بین 0 تا 40 انتخاب کنید !")
                # add the user's numbers to the list of participants
                if not Message.from_user.first_name in participants.keys():
                    participants[Message.from_user.first_name] = user_numbers
                    await subtraction(Message.from_user.id,40.0)
                    await Client.send_message(Message.chat.id, f"📝✿ | اعداد {Message.from_user.first_name} با موفقیت ثبت شدند! ⬱{user_numbers}")
                    nameid[Message.from_user.first_name] = Message.from_user.id
                else:
                    raise ValueError(f"！ | شما قبلا اعدادی را انتخاب کردین ! {participants[Message.from_user.first_name]} ")
            except ValueError as e:
                await Message.reply(str(e))
        else:
            pass




