from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatAction
import asyncio, random

TOKEN = "8614015067:AAG2Jb0OgRH06gtuu1ybTOM2FTLzdwsuyCE"
OWNER_ID = 8625848837
CHANNEL_LINK = "https://t.me/+uK3bdZ68BmhmMWM1"

users = {}
user_map = {}

def join_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Join Channel", url=CHANNEL_LINK)]])

def ensure_user(user):
    uid = user.id
    name = f"{user.first_name} {user.last_name or ''}".strip()
    users[uid] = {"name": name}
    return uid

async def delete_msg(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.delete_message(
            chat_id=context.job.data["chat_id"],
            message_id=context.job.data["message_id"]
        )
    except:
        pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user)

    name = users[user.id]["name"]

    await update.message.reply_text(
        f"👋 Welcome {name} !\n\n"
        "💼 Thank you for contacting our support\n"
        "📩 Your request has been received\n\n"
        "🎯 Join our official channel:\n"
        f"🚀 {CHANNEL_LINK}\n\n"
        "Note :- You can submit earning proof and ask queries related to offers ❤️👍",
        reply_markup=join_button()
    )

async def owner_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    if update.message.reply_to_message:
        mid = update.message.reply_to_message.message_id
        if mid in user_map:
            await context.bot.send_message(chat_id=user_map[mid], text=update.message.text)

# 🎤 VOICE (10 Hindi + 10 English)
voice_replies = [
f"🎤 {name}, आपका वॉइस संदेश प्राप्त हो गया है\nकृपया थोड़ा प्रतीक्षा करें, हम सुनकर उत्तर देंगे 🙂",
f"🔊 {name}, आपकी आवाज़ स्पष्ट रूप से मिल गई है\nजांच करके जल्द ही जवाब देंगे 👍",
f"🎧 {name}, आपका वॉइस नोट मिल चुका है\nअभी ध्यान से सुन रहे हैं ⏳",
f"📩 {name}, आपका वॉइस संदेश प्राप्त हुआ है\nजल्द ही आपको उत्तर मिलेगा 💬",
f"🎤 {name}, आपकी बात हमें सुनाई दे रही है\nकृपया थोड़ा समय दें 🙏",
f"🔊 {name}, आपका वॉइस नोट सफलतापूर्वक मिल गया है\nजांच जारी है 🔄",
f"🎧 {name}, आपकी आवाज़ सुन ली गई है\nउत्तर तैयार किया जा रहा है 😊",
f"📩 {name}, आपका संदेश प्राप्त हो चुका है\nअभी प्रक्रिया चल रही है ⚡",
f"🎤 {name}, आपकी रिकॉर्डिंग मिल गई है\nजल्द ही उत्तर दिया जाएगा 👍",
f"🔊 {name}, आपकी आवाज़ स्पष्ट है\nहम जल्द ही प्रतिक्रिया देंगे 💬",

f"🎤 {name}, your voice message has been received\nPlease wait while we listen and respond 🙂",
f"🔊 {name}, your voice is clear\nWe will reply after checking 👍",
f"🎧 {name}, your voice note is received\nListening carefully now ⏳",
f"📩 {name}, we got your voice message\nResponse will be sent shortly 💬",
f"🎤 {name}, your message is heard clearly\nPlease give us a moment 🙏",
f"🔊 {name}, voice received successfully\nProcessing it now 🔄",
f"🎧 {name}, we are listening to your audio\nReply coming soon 😊",
f"📩 {name}, your voice note arrived\nWorking on it ⚡",
f"🎤 {name}, your recording is here\nWe will respond shortly 👍",
f"🔊 {name}, message received loud and clear\nReplying soon 💬"
]

# 🎧 AUDIO
audio_replies = [
f"🎧 {name}, आपका ऑडियो प्राप्त हो गया है\nकृपया थोड़ा इंतज़ार करें 🙂",
f"🔊 {name}, ऑडियो फ़ाइल सफलतापूर्वक मिल गई है\nजांच जारी है 👍",
f"🎶 {name}, आपका ऑडियो स्पष्ट है\nहम सुनकर उत्तर देंगे ⏳",
f"📩 {name}, ऑडियो प्राप्त हो चुका है\nअभी प्रक्रिया चल रही है 💬",
f"🎧 {name}, आपकी फ़ाइल मिल गई है\nजल्द ही उत्तर मिलेगा 😊",
f"🔊 {name}, ऑडियो सुरक्षित रूप से प्राप्त हुआ है\nजांच कर रहे हैं 🔄",
f"🎶 {name}, आपका ऑडियो सुन रहे हैं\nकृपया प्रतीक्षा करें ⚡",
f"📩 {name}, ऑडियो फ़ाइल आ गई है\nउत्तर जल्द दिया जाएगा 👍",
f"🎧 {name}, आपकी ऑडियो मिल गई है\nथोड़ा समय दें 🙏",
f"🔊 {name}, ऑडियो स्पष्ट रूप से प्राप्त हुआ है\nप्रक्रिया जारी है 💬",

f"🎧 {name}, your audio file has been received\nPlease wait for a moment 🙂",
f"🔊 {name}, audio received successfully\nChecking it now 👍",
f"🎶 {name}, your audio is clear\nListening carefully ⏳",
f"📩 {name}, your file is here\nProcessing it 💬",
f"🎧 {name}, we got your audio\nReply will be sent soon 😊",
f"🔊 {name}, file received safely\nChecking details 🔄",
f"🎶 {name}, listening to your audio\nPlease wait ⚡",
f"📩 {name}, audio arrived\nResponse coming 👍",
f"🎧 {name}, your file is ready\nGive us a moment 🙏",
f"🔊 {name}, audio received clearly\nReplying soon 💬"
]

# 🎥 VIDEO
video_replies = [
f"🎥 {name}, आपका वीडियो प्राप्त हो गया है\nअभी देख रहे हैं 🙂",
f"📹 {name}, वीडियो सफलतापूर्वक मिल गया है\nजांच जारी है 👍",
f"🎬 {name}, आपका क्लिप प्राप्त हुआ है\nकृपया प्रतीक्षा करें ⏳",
f"📩 {name}, वीडियो मिल चुका है\nअभी प्रक्रिया चल रही है 💬",
f"🎥 {name}, आपका वीडियो देख लिया गया है\nजल्द उत्तर देंगे 😊",
f"📹 {name}, वीडियो स्पष्ट रूप से प्राप्त हुआ है\nजांच कर रहे हैं 🔄",
f"🎬 {name}, क्लिप आ गया है\nउत्तर जल्द मिलेगा ⚡",
f"📩 {name}, वीडियो सुरक्षित मिला है\nअभी देख रहे हैं 👍",
f"🎥 {name}, आपका वीडियो खोल लिया गया है\nथोड़ा समय दें 🙏",
f"📹 {name}, वीडियो प्राप्त हो गया है\nप्रक्रिया जारी है 💬",

f"🎥 {name}, your video has been received\nWatching it now 🙂",
f"📹 {name}, video received successfully\nChecking details 👍",
f"🎬 {name}, your clip arrived\nPlease wait ⏳",
f"📩 {name}, video is here\nProcessing it 💬",
f"🎥 {name}, watching your video\nReply soon 😊",
f"📹 {name}, video came clearly\nChecking now 🔄",
f"🎬 {name}, clip received\nResponse coming ⚡",
f"📩 {name}, your video is ready\nReviewing it 👍",
f"🎥 {name}, got your footage\nGive us a moment 🙏",
f"📹 {name}, video received clearly\nReplying soon 💬"
]

# 📸 PHOTO
photo_replies = [
f"📸 {name}, आपकी फोटो प्राप्त हो गई है\nअभी देख रहे हैं 🙂",
f"🖼️ {name}, आपका स्क्रीनशॉट सफलतापूर्वक मिल गया है\nजांच कर रहे हैं 👍",
f"📷 {name}, आपकी तस्वीर स्पष्ट है\nकृपया प्रतीक्षा करें ⏳",
f"📩 {name}, फोटो मिल चुकी है\nअभी प्रक्रिया चल रही है 💬",
f"📸 {name}, आपकी photo देख ली गई है\nजल्द उत्तर देंगे 😊",
f"🖼️ {name}, आपका स्क्रीनशॉट सुरक्षित प्राप्त हुआ है\nजांच जारी है 🔄",
f"📷 {name}, आपकी फोटो मिल गई है\nउत्तर जल्द मिलेगा ⚡",
f"📩 {name}, आपका स्क्रीनशॉट आ गया है\nअभी देख रहे हैं 👍",
f"📸 {name}, आपकी फोटो खोल ली गई है\nथोड़ा समय दें 🙏",
f"🖼️ {name}, आपका स्क्रीनशॉट प्राप्त हो गया है\nप्रक्रिया जारी है 💬",

f"📸 {name}, your photo has been received\nViewing it now 🙂",
f"🖼️ {name}, image received successfully\nChecking details 👍",
f"📷 {name}, your picture is clear\nPlease wait ⏳",
f"📩 {name}, image is here\nProcessing it 💬",
f"📸 {name}, viewing your photo\nReply soon 😊",
f"🖼️ {name}, image came clearly\nChecking now 🔄",
f"📷 {name}, photo received\nResponse coming ⚡",
f"📩 {name}, your image is ready\nReviewing it 👍",
f"📸 {name}, got your picture\nGive us a moment 🙏",
f"🖼️ {name}, image received clearly\nReplying soon 💬"
]

# 💬 TEXT
text_replies = [
f"💬 {name}, आपका संदेश प्राप्त हो गया है\nअभी पढ़ रहे हैं 🙂",
f"📩 {name}, आपका संदेश मिल गया है\nजांच कर रहे हैं 👍",
f"✉️ {name}, आपका टेक्स्ट प्राप्त हुआ है\nकृपया प्रतीक्षा करें ⏳",
f"📨 {name}, संदेश मिल चुका है\nअभी प्रक्रिया चल रही है 💬",
f"💬 {name}, आपका संदेश पढ़ लिया गया है\nजल्द उत्तर देंगे 😊",
f"📩 {name}, संदेश स्पष्ट रूप से मिला है\nजांच जारी है 🔄",
f"✉️ {name}, आपका टेक्स्ट मिल गया है\nउत्तर जल्द मिलेगा ⚡",
f"📨 {name}, संदेश आ गया है\nअभी देख रहे हैं 👍",
f"💬 {name}, आपका संदेश खोल लिया गया है\nथोड़ा समय दें 🙏",
f"📩 {name}, संदेश सुरक्षित प्राप्त हुआ है\nप्रक्रिया जारी है 💬",

f"💬 {name}, your message has been received\nReading it now 🙂",
f"📩 {name}, message received successfully\nChecking details 👍",
f"✉️ {name}, your text came through\nPlease wait ⏳",
f"📨 {name}, message is here\nProcessing it 💬",
f"💬 {name}, reading your message\nReply soon 😊",
f"📩 {name}, message came clearly\nChecking now 🔄",
f"✉️ {name}, text received\nResponse coming ⚡",
f"📨 {name}, your message is ready\nReviewing it 👍",
f"💬 {name}, got your text\nGive us a moment 🙏",
f"📩 {name}, message received clearly\nReplying soon 💬"
]

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    uid = ensure_user(user)

    if uid == OWNER_ID:
        return

    fwd = await context.bot.forward_message(
        chat_id=OWNER_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    user_map[fwd.message_id] = uid

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    # ✅ THIS LINE WAS MISSING
    asyncio.create_task(auto_reply(update, context))


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await asyncio.sleep(5)

    if not update.message:
        return

 # ✅ NAME YAHAN ADD KAR
    name = f"{update.effective_user.first_name}"
    
    if update.message.voice:
        text = random.choice(voice_replies)
    elif update.message.audio:
        text = random.choice(audio_replies)
    elif update.message.video:
        text = random.choice(video_replies)
    elif update.message.photo:
        text = random.choice(photo_replies)
    else:
        text = random.choice(text_replies)

    # ✅ SEND MESSAGE
    msg = await update.message.reply_text(text)

    # ✅ AUTO DELETE FUNCTION
    async def auto_delete():
        await asyncio.sleep(5)
        try:
            await msg.delete()
        except:
            pass

    asyncio.create_task(auto_delete())

    
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, owner_reply))
app.add_handler(MessageHandler(filters.ALL, handle))

print("🔥 FINAL PRO BOT RUNNING...")
app.run_polling()