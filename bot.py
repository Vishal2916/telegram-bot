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

voice_replies = ["🎤 Voice received", "🔊 Voice note received"]
audio_replies = ["🎧 Audio received", "🔊 Audio file received"]
video_replies = ["🎥 Video received", "📹 Video received"]
photo_replies = ["📸 Image received", "🖼️ Screenshot received"]
text_replies = ["💬 Message received", "📩 Got your message"]

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

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    await asyncio.sleep(random.randint(6, 8))

    if update.message.voice:
        msg = await update.message.reply_text(random.choice(voice_replies))
    elif update.message.audio:
        msg = await update.message.reply_text(random.choice(audio_replies))
    elif update.message.video:
        msg = await update.message.reply_text(random.choice(video_replies))
    elif update.message.photo:
        msg = await update.message.reply_text(random.choice(photo_replies))
    else:
        msg = await update.message.reply_text(random.choice(text_replies))

    context.job_queue.run_once(delete_msg, random.randint(5, 6), data={
        "chat_id": msg.chat_id,
        "message_id": msg.message_id
    })

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, owner_reply))
app.add_handler(MessageHandler(filters.ALL, handle))

print("🔥 FINAL BOT RUNNING...")
app.run_polling()
