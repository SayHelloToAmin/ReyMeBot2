import db



async def lvlup(Client,Message,text):
    userid = Message.from_user.id
    Cloud = db.getxp(userid)
    if Cloud[1] - Cloud[0] > 0:
        await Message.reply("""😭 | متاسفانه کصپی کافی برای لول اپ نداری. کصپی های فعلیت ⬱ / mylevel
""")
    else:
        level = db.getlevel(userid)
        Cloud2 = Cloud[1] - Cloud[0]
        try:
            db.upxp(userid,Cloud2)
        except:
            await Message.reply("😱 | یه مشکلی پیش اومده ꉕ ")
        else:
            try:
                db.uplevel(userid)
            except:
                db.upxp(userid,Cloud)
                await Message.reply("😱 | یه مشکلی پیش اومده ꉕ ")
            else:
                try:
                    db.upneedxp(userid)
                except:
                    db.upxp(userid,Cloud)
                    db.downlevel(userid)
                else:
                    await Message.reply(f"""🎉 | تبریک میگم پدسگ به لول {level+1} خوش اومدی . الان میتونی لولای زیریت یا شاید هم سطحتو انگشت کنی ꆛ """)



