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
"🎤 Voice mila, check kar rahe hain","🔊 Aapka voice note receive ho gaya","🎧 Voice aa gaya, thoda wait karein","📩 Voice message mil gaya","🎤 Aapka voice sun rahe hain","🔊 Voice successfully receive hua","🎧 Aapka audio note mil gaya","📩 Voice note process ho raha hai","🎤 Voice received, checking","🔊 Voice note received",
"🎤 Got your voice message","🔊 Voice received successfully","🎧 Listening to your voice","📩 Voice message received","🎤 Your voice note is here","🔊 Voice message captured","🎧 Audio note received","📩 Voice processing started","🎤 We got your voice","🔊 Voice noted"
]

# 🎧 AUDIO
audio_replies = [
"🎧 Audio file mil gaya","🔊 Aapka audio receive ho gaya","🎶 Audio check kar rahe hain","📩 Audio mil gaya","🎧 Aapka music/audio aa gaya","🔊 Audio file successfully receive hua","🎶 Audio sun rahe hain","📩 Audio process ho raha hai","🎧 Audio received, checking","🔊 Audio file received",
"🎧 Got your audio file","🔊 Audio received successfully","🎶 Listening to your audio","📩 Audio file received","🎧 Your audio is here","🔊 Audio captured","🎶 Audio noted","📩 Processing your audio","🎧 Audio received","🔊 Audio done"
]

# 🎥 VIDEO
video_replies = [
"🎥 Video mil gaya","📹 Aapka video receive ho gaya","🎬 Video check kar rahe hain","📩 Video mil gaya","🎥 Aapka clip aa gaya","📹 Video successfully receive hua","🎬 Video dekh rahe hain","📩 Video process ho raha hai","🎥 Video received, checking","📹 Video file received",
"🎥 Got your video","📹 Video received successfully","🎬 Watching your video","📩 Video received","🎥 Your video is here","📹 Video captured","🎬 Video noted","📩 Processing video","🎥 Video received","📹 Video done"
]

# 📸 PHOTO
photo_replies = [
"📸 Image mil gayi","🖼️ Screenshot receive ho gaya","📷 Photo check kar rahe hain","📩 Image mil gayi","📸 Aapki photo aa gayi","🖼️ Image successfully receive hui","📷 Photo dekh rahe hain","📩 Image process ho rahi hai","📸 Photo received, checking","🖼️ Image file received",
"📸 Got your image","🖼️ Image received successfully","📷 Viewing your photo","📩 Image received","📸 Your picture is here","🖼️ Image captured","📷 Photo noted","📩 Processing image","📸 Image received","🖼️ Image done"
]

# 💬 TEXT
text_replies = [
"💬 Message mil gaya","📩 Aapka msg receive ho gaya","✉️ Message check kar rahe hain","📨 Msg mil gaya","💬 Aapka text aa gaya","📩 Message successfully receive hua","✉️ Msg padh rahe hain","📨 Message process ho raha hai","💬 Text received, checking","📩 Message received",
"💬 Got your message","📩 Message received successfully","✉️ Reading your text","📨 Text received","💬 Your message is here","📩 Message captured","✉️ Text noted","📨 Processing message","💬 Message received","📩 Done reading"
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

    # 👇 ADD THIS LINE
    asyncio.create_task(auto_reply(update, context))


# ✅ OUTSIDE (same level as handle)
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await asyncio.sleep(5)

    user = update.effective_user
    name = f"{user.first_name} {user.last_name or ''}".strip()
    uid = user.id

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

    context.application.job_queue.run_once(
        delete_msg,
        5,
        data={
            "chat_id": msg.chat_id,
            "message_id": msg.message_id
        }
    )
    
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, owner_reply))
app.add_handler(MessageHandler(filters.ALL, handle))

print("🔥 FINAL PRO BOT RUNNING...")
app.run_polling()