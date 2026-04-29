from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatAction
import asyncio, random
asyncio.get_event_loop().close()

TOKEN = "8614015067:AAG2Jb0OgRH06gtuu1ybTOM2FTLzdwsuyCE"
OWNER_ID = 8625848837
CHANNEL_LINK = "https://t.me/+uK3bdZ68BmhmMWM1"

users = {}
user_map = {}
shown_users = set()

# ---------- BUTTON ----------
def join_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Join Channel", url=CHANNEL_LINK)]
    ])

# ---------- USER ----------
def ensure_user(user):
    uid = user.id
    name = f"{user.first_name} {user.last_name or ''}".strip()

    if uid not in users:
        users[uid] = {"name": name, "msg": 0, "photo": 0}

    return uid

# ---------- DELETE ----------
async def delete_msg(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.delete_message(
            chat_id=context.job.data["chat_id"],
            message_id=context.job.data["message_id"]
        )
    except:
        pass

# ---------- START (GREETING SAME AS IMAGE) ----------
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

# ---------- OWNER REPLY ----------
async def owner_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if not update.message.reply_to_message:
        return

    mid = update.message.reply_to_message.message_id

    if mid in user_map:
        await context.bot.send_message(
            chat_id=user_map[mid],
            text=update.message.text
        )

# ---------- REPLIES (ALL 20 ADDED) ----------

voice_replies = [
"🎤 आपका वॉइस संदेश प्राप्त हो गया है\nमैं इसे सुनकर शीघ्र उत्तर दूंगा 🙂",
"🔊 आपकी आवाज़ मिल गई है\nकृपया थोड़ी देर प्रतीक्षा करें 🙏",
"🎧 वॉइस नोट प्राप्त हुआ है\nजांच के बाद उत्तर दिया जाएगा ⏳",
"📢 आपकी रिकॉर्डिंग मिल गई है\nमैं सुनकर प्रतिक्रिया दूंगा 👍",
"🎙️ आपका वॉइस मैसेज प्राप्त हुआ\nकृपया थोड़ा समय दें 😊",
"🎤 आपकी आवाज़ सफलतापूर्वक प्राप्त हुई\nमैं जल्द ही जवाब दूंगा 🚀",
"🔊 वॉइस मैसेज मिल गया है\nमैं इसे सुन रहा हूँ 🕐",
"🎧 आपका वॉइस नोट रिकॉर्ड हुआ\nउत्तर शीघ्र मिलेगा ✔️",
"📢 आपकी ऑडियो रिकॉर्डिंग प्राप्त हुई\nजांच जारी है 🔍",
"🎙️ वॉइस संदेश मिल गया है\nकृपया प्रतीक्षा करें 😄",
"🎤 Your voice message has been received\nI will listen and reply shortly 🙂",
"🔊 Voice note received successfully\nPlease wait while I review it 🙏",
"🎧 Got your voice message\nI’ll listen and respond soon ⏳",
"📢 Your recording has been received\nChecking now 👍",
"🎙️ Voice message noted\nKindly wait for my response 😊",
"🎤 Voice received successfully\nI’ll get back to you soon 🚀",
"🔊 Your voice note is received\nReviewing it now 🕐",
"🎧 Got your audio message\nResponse will be sent shortly ✔️",
"📢 Voice recording received\nVerification in progress 🔍",
"🎙️ Message received clearly\nPlease hold on 😄"
]

audio_replies = [
"🎧 आपका ऑडियो प्राप्त हो गया है\nमैं सुनकर उत्तर दूंगा 🙂",
"🔊 ऑडियो फाइल मिल गई है\nकृपया प्रतीक्षा करें 🙏",
"🎶 आपका ऑडियो नोट प्राप्त हुआ\nजांच जारी है ⏳",
"📀 ऑडियो सफलतापूर्वक प्राप्त हुआ\nउत्तर शीघ्र मिलेगा 👍",
"🎵 आपकी फाइल मिल गई है\nमैं इसे सुन रहा हूँ 😊",
"🎧 ऑडियो रिकॉर्डिंग प्राप्त हुई\nथोड़ा समय दें 🚀",
"🔊 ऑडियो संदेश मिल गया है\nजांच कर रहा हूँ 🕐",
"🎶 आपकी ऑडियो फाइल नोट की गई\nउत्तर दिया जाएगा ✔️",
"📀 ऑडियो प्राप्त हुआ है\nसत्यापन जारी है 🔍",
"🎵 आपका ऑडियो सफलतापूर्वक मिला\nकृपया प्रतीक्षा करें 😄",
"🎧 Your audio has been received\nI will review it shortly 🙂",
"🔊 Audio file received successfully\nPlease wait 🙏",
"🎶 Got your audio file\nChecking it now ⏳",
"📀 Audio received\nI’ll respond soon 👍",
"🎵 Your audio is noted\nReviewing now 😊",
"🎧 Audio recording received\nResponse coming soon 🚀",
"🔊 Your audio message is received\nChecking now 🕐",
"🎶 Audio file noted\nReply will be sent ✔️",
"📀 Audio received successfully\nVerification in progress 🔍",
"🎵 Your audio has been recorded\nPlease wait 😄"
]

video_replies = [
"🎥 आपका वीडियो प्राप्त हो गया है\nमैं देखकर उत्तर दूंगा 🙂",
"📹 वीडियो मिल गया है\nकृपया प्रतीक्षा करें 🙏",
"🎬 आपकी क्लिप प्राप्त हुई है\nजांच जारी है ⏳",
"📽️ वीडियो सफलतापूर्वक मिला\nउत्तर शीघ्र मिलेगा 👍",
"🎞️ आपका वीडियो मिल गया है\nमैं देख रहा हूँ 😊",
"🎥 वीडियो रिकॉर्डिंग प्राप्त हुई\nथोड़ा समय दें 🚀",
"📹 वीडियो संदेश मिल गया है\nजांच कर रहा हूँ 🕐",
"🎬 वीडियो नोट किया गया है\nउत्तर दिया जाएगा ✔️",
"📽️ वीडियो प्राप्त हुआ है\nसत्यापन जारी है 🔍",
"🎞️ आपकी वीडियो फाइल मिल गई\nकृपया प्रतीक्षा करें 😄",
"🎥 Your video has been received\nI will watch and reply shortly 🙂",
"📹 Video received successfully\nPlease wait 🙏",
"🎬 Got your video\nReviewing now ⏳",
"📽️ Video received\nI’ll respond soon 👍",
"🎞️ Your video is noted\nChecking now 😊",
"🎥 Video recording received\nReply coming soon 🚀",
"📹 Your video message is received\nReviewing now 🕐",
"🎬 Video noted\nResponse will be sent ✔️",
"📽️ Video received successfully\nVerification in progress 🔍",
"🎞️ Your video has been recorded\nPlease wait 😄"
]

photo_replies = [
"📸 आपकी तस्वीर प्राप्त हो गई है\nमैं जांचकर उत्तर दूंगा 🙂",
"🖼️ स्क्रीनशॉट मिल गया है\nकृपया प्रतीक्षा करें 🙏",
"📷 आपकी इमेज प्राप्त हुई\nजांच जारी है ⏳",
"📸 फोटो सफलतापूर्वक मिला\nउत्तर शीघ्र मिलेगा 👍",
"🖼️ आपकी तस्वीर मिल गई है\nमैं देख रहा हूँ 😊",
"📷 इमेज प्राप्त हुई है\nथोड़ा समय दें 🚀",
"📸 स्क्रीनशॉट मिल गया है\nजांच कर रहा हूँ 🕐",
"🖼️ आपकी इमेज नोट की गई\nउत्तर दिया जाएगा ✔️",
"📷 फोटो प्राप्त हुआ है\nसत्यापन जारी है 🔍",
"📸 आपकी तस्वीर मिल गई\nकृपया प्रतीक्षा करें 😄",
"📸 Your screenshot has been received\nI will review it shortly 🙂",
"🖼️ Image received successfully\nPlease wait 🙏",
"📷 Got your image\nChecking now ⏳",
"📸 Screenshot received\nI’ll respond soon 👍",
"🖼️ Your image is noted\nReviewing now 😊",
"📷 Image received\nReply coming soon 🚀",
"📸 Your screenshot is received\nChecking now 🕐",
"🖼️ Image noted\nResponse will be sent ✔️",
"📷 Image received successfully\nVerification in progress 🔍",
"📸 Your screenshot is recorded\nPlease wait 😄"
]

text_replies = [
"👋 Hey {name}, Your Message has been received,\nKindly wait for my reply",
"💬 Message received, please wait",
"📩 Got your message, checking now",
"📝 Message noted, reply soon",
"📨 Message received successfully",
"💬 Processing your message",
"📩 Checking your message",
"📝 Reply will be sent soon",
"📨 Wait for response",
"💬 Message accepted",

"👋 आपका संदेश प्राप्त हो गया है\nकृपया प्रतीक्षा करें",
"💬 मैसेज मिल गया",
"📩 संदेश प्राप्त हुआ",
"📝 संदेश नोट हुआ",
"📨 मैसेज सफलतापूर्वक मिला",
"💬 प्रोसेस हो रहा है",
"📩 जांच जारी है",
"📝 उत्तर जल्द मिलेगा",
"📨 कृपया प्रतीक्षा करें",
"💬 संदेश स्वीकार हुआ"
]

# ---------- MAIN ----------
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    uid = ensure_user(user)
    name = users[uid]["name"]

    if uid == OWNER_ID:
        return

    if update.message.photo:
        users[uid]["photo"] += 1
    else:
        users[uid]["msg"] += 1

    if uid not in shown_users:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"👤 {name}\n🆔 <tg-spoiler>{uid}</tg-spoiler>",
            parse_mode="HTML"
        )
        shown_users.add(uid)

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

    await asyncio.sleep(2)

    if update.message.voice:
        msg = await update.message.reply_text(random.choice(voice_replies))
    elif update.message.audio:
        msg = await update.message.reply_text(random.choice(audio_replies))
    elif update.message.video:
        msg = await update.message.reply_text(random.choice(video_replies))
    elif update.message.photo:
        msg = await update.message.reply_text(random.choice(photo_replies))
    else:
        msg = await update.message.reply_text(random.choice(text_replies).replace("{name}", name))

    context.job_queue.run_once(delete_msg, 8, data={
        "chat_id": msg.chat_id,
        "message_id": msg.message_id
    })

# ---------- RUN ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, owner_reply))
app.add_handler(MessageHandler(filters.ALL, handle))

print("🔥 BOT RUNNING PERFECT...")

app.run_polling(
    drop_pending_updates=True,
    allowed_updates=Update.ALL_TYPES
)