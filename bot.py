from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_LINK = "https://t.me/+uK3bdZ68BmhmMWM1"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    text = f"""👋 Welcome {user} !

💼 Thank you for contacting our support  
📩 Your request has been received  

🎯 Join our official channel:
🚀 {CHANNEL_LINK}

Note :- You can submit earning proof and ask queries related to offers ❤️👍
"""

    keyboard = [
        [InlineKeyboardButton("🚀 Join Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, reply_markup=reply_markup)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot running 🚀")
    app.run_polling()

# ✅ FIX HERE
if __name__ == "__main__":
    main()