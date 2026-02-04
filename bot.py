import os
import yt_dlp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

# زانیارییەکانی تۆ
API_ID = 20718200
API_HASH = "da1eb90b9a9e7b49affa35a1b397f1f8"
BOT_TOKEN = "8494295341:AAFUxoDcPdG1_ItBvlHN_OY6R8jd_eFuHF4"
SESSION = "AgBNbLcATOoIydAmO13kBVHRmXYT3iv-XFkg3BWDLxrM0UZylx2NSyg8fR-Kz0cO2047jGXbJjT5QZRdyzSZtB9lqT4-kaCyXSqP1nCz_QVwq3c_9W2CCOGHGP1W3T0zruP_2heIisr4wuRhIm23-tiTg3qNiSQAr13ozllN8EfLXjZ4MOSQ5utFBF1CrFf4-gFa5CLxSJLdeE_9Kxq8DNp10RUhv2N4P-uFCwC-5BDHjTlOn-_IdVPc_A5d_90oDUc9VQgIeOlLXQSP_2iq-F0bj1foFCYVm-ojiM7b-r02s3IoqHWCgPAXGV0_c4hwesQ822ZKfg9lQLHAL31o_wkQXNtAPgAAAAGp7OapAA"

app = Client("TiktokBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
# زیادکردنی سێشن بۆ ئەکاونتە یارمەتیدەرەکە
assistant = Client("Assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

call_py = PyTgCalls(assistant)

@app.on_message(filters.command("play") & filters.group)
async def play_audio(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ لینکی تیکتۆک بنێرە.\nنموونە: `/play link`")
    
    url = message.text.split(None, 1)[1]
    msg = await message.reply("⏳ خەریکم ئامادەی دەکەم...")
    
    ydl_opts = {'format': 'bestaudio', 'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            title = info['title']
        except Exception as e:
            return await msg.edit(f"❌ کێشەیەک لە لینکەکە هەیە: {e}")

    try:
        await call_py.join_group_call(
            message.chat.id,
            AudioPiped(audio_url)
        )
        await msg.edit(f"🎶 **پەخش دەکرێت:**\n`{title}`")
    except Exception as e:
        await msg.edit(f"❌ کێشە لە چوونە ناو کاڵ: {e}")

@app.on_message(filters.command("stop") & filters.group)
async def stop_audio(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply("⏹ پەخشەکە وەستا.")
    except:
        await message.reply("❌ بۆتەکە لە کاڵ نییە.")

# دەستپێکردنی هەموو خزمەتگوزارییەکان
print("بۆتەکە دەستی پێکرد...")
assistant.start()
app.start()
call_py.run()
