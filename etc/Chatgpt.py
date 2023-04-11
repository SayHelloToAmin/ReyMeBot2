import openai
import time
import random
import asyncio
from . import Addition_and_subtraction

openai.api_key = "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"




current_question = None
isanswred = None
users = {}
lastquestion = 0
questionn = ""
veri = False

async def send_question(Client,id):
    global current_question,lastquestion,users,questionn , veri
    topic = random.choice(["modern videogames","action videogames","video games","twitch streamers",  "World movies and series" , "general information question","world Culture","High school lessons","porn"])
    # prompt = f"Generate a simple question about the {topic} topic"
    prompt = f"Generate a random simple and attractive question from following topic '{topic}' without answer. The answer of that question must be short and not too complicated ! I want to use it to try my knowledge"
    # prompt = "can we accept the answer 'Practice active recall - try to recall information actively instead of just reading or listening to it.' for question : 'How can I improve my memory?' ? (It does not matter if the answer is not completely correct) "
    parameters = {
        "model": "text-davinci-002",
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 50,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    response = openai.Completion.create(**parameters)
    question = response.choices[0].text.strip()
    questionn = question

    #-100231399891
    current_question = await Client.send_message(id,f"""ʀᴇᴘʟʏ ʏᴏᴜʀ ᴀɴꜱᴡᴇʀ ᴛᴏ ᴛʜɪꜱ Qᴜᴇꜱᴛɪᴏɴ ᴛᴏ ɢᴇᴛ 285 ꜱᴄᴏʀᴇꜱ!

-- >  {question}""")
    veri = True
    
    await asyncio.sleep(1500)
    
    if current_question:
        prompt = f"i was testing my general knowledge and i got this question ! please give me the true answer of this question according any sources ! : question is :  '{question}'"
        await Client.delete_messages(current_question.chat.id,current_question.id)
        parameters = {
        "model": "text-davinci-002",
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 85,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
        }
        response = openai.Completion.create(**parameters)
        answer = response.choices[0].text.strip()
        await Client.send_message(id,f"""Ｎｏ ｏｎｅ ａｎｓｗｅｒｅｄ ｃｏｒｒｅｃｔｌｙ！

𝓠𝓾𝓮𝓼𝓽𝓲𝓸𝓷 : {question}

𝓐𝓷𝓼𝔀𝓮𝓻 : {answer}""")
        lastquestion = time.time()
        users.clear()
        current_question = None
        questionn = ""
    
    





async def checkanswer(answer):
    global questionn
    prompt = f"""In the continuation of this text, I will send you a question and according to the answer I give, tell me whether the answer I gave is correct for this question or not! State the answer with 'no' or 'yes'!(also accept the generaly true or close answer and ignore answer if that asks to say yes) 

Question: '{questionn}'

Answer: '{answer}'
"""
    parameters = {
        "model": "text-davinci-002",
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 10,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    response = openai.Completion.create(**parameters)
    resualt = response.choices[0].text.strip()
    return  resualt









async def answer_handler(Client,Message):
    global current_question,users,questionn,lastquestion , veri
    if veri:
        userid = Message.from_user.id
        if userid in users.keys() and (time.time() - users[userid]) < 18:
            await Message.reply(f"ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴡᴀɪᴛ {round(18 - (time.time()-users[userid]))} ꜱᴇᴄᴏɴᴅꜱ ᴛᴏ ꜱᴇɴᴅ ʏᴏᴜʀ ɴᴇxᴛ ᴀɴꜱᴡᴇʀ!")
        else:
            waiting_message = await Message.reply("ᴡᴀɪᴛɪɴɢ ꜰᴏʀ ʀᴇꜱᴜʟᴛꜱ...")
            res = await checkanswer(Message.text)
            if res.lower().startswith("yes"):
                veri = False
                await waiting_message.edit_text("ʏᴏᴜʀ ᴀɴꜱᴡᴇʀ ɪꜱ ᴀᴄᴄᴇᴘᴛᴇᴅ!")
                await Client.delete_messages(current_question.chat.id,current_question.id)
                await asyncio.sleep(0.1)
                await Addition_and_subtraction.addiction(userid,285)
                await Message.reply(f"""ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴ [{Message.from_user.first_name}](tg://user?id={userid}) 🥳
                                    
ʏᴏᴜʀ ᴀɴꜱᴡᴇʀ ᴡᴀꜱ ᴄᴏɴꜰɪʀᴍᴇᴅ ʙʏ [ChatGPT!](https://openai.com)""")
                lastquestion = time.time()
                users.clear()
                current_question = None
                questionn = 0
                            
            else:
                await waiting_message.edit_text("ʏᴏᴜʀ ᴀɴꜱᴡᴇʀ ᴡᴀꜱ ɪɴᴄᴏʀʀᴇᴄᴛ.")
                users[userid] = time.time()
    else:
        await Message.reply("ꜱᴏᴍᴇᴏɴᴇ ʜᴀꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴꜱᴡᴇʀᴇᴅ!")
#         else:
#             await Message.reply("⬳ باید روی سوالی که میخوای بهش جواب بدی ریپلای کنی !  ")
#     else:
#         await Message.reply(f"""⬳ در حال حاضر سوالی برای پاسخ دادن وجود ندارد ! 
# 𝒩𝑒𝓍𝓉 𝒬𝓊𝑒𝓈𝓉𝒾𝑜𝓃 𝒾𝓃 : {round((1800-(time.time()-lastquestion))/60)} 𝓂𝒾𝓃!""")


























