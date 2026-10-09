import asyncio
import logging
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# आपका BotFather API Token
BOT_TOKEN = "8951896304:AAESNXbtBWTAZpd7RdbBJ4gsSvcZE_lxT3k"

user_reminder_tasks = {}


async def send_reminder(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await asyncio.sleep(30)
    if chat_id in user_reminder_tasks:
        reminder_text = (
            "अरे गेमर! 🎮 ऐसा लगता है आपने अभी तक अपना mobile number नहीं भेजा है। "
            "गेमिंग अकाउंट तुरंत चालू करने के लिए कृपया अपना 10 अंकों का मोबाइल नंबर यहाँ टाइप करके भेजें! 👇"
        )
        await context.bot.send_message(chat_id=chat_id, text=reminder_text)
        del user_reminder_tasks[chat_id]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id in user_reminder_tasks:
        user_reminder_tasks[chat_id].cancel()

    welcome_text = (
        "नमस्ते गेमर! 👋 हमारे साथ अपना गेमिंग अकाउंट बनाने के लिए "
        "कृपया अपना 10 अंकों का मोबाइल नंबर यहाँ टाइप करके भेजें:👇"
    )
    await update.message.reply_text(welcome_text)

    task = asyncio.create_task(send_reminder(context, chat_id))
    user_reminder_tasks[chat_id] = task


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text.strip()

    digits_only = re.sub(r"\D", "", user_text)
    if digits_only.startswith("91") and len(digits_only) == 12:
        digits_only = digits_only[2:]

    is_valid_phone = re.match(r"^[6-9]\d{9}$", digits_only)

    if is_valid_phone:
        if chat_id in user_reminder_tasks:
            user_reminder_tasks[chat_id].cancel()
            del user_reminder_tasks[chat_id]

        thank_you_text = (
            "धन्यवाद! 🎮 आपका नंबर हमारे पास सुरक्षित दर्ज हो गया है। "
            "हमारी टीम जल्द ही आपसे संपर्क करके आपका गेमिंग अकाउंट चालू कर देगी। 👍"
        )
        await update.message.reply_text(thank_you_text)
        logging.info(f"NEW LEAD CAPTURED: Chat ID: {chat_id} | Phone: {digits_only}")
    else:
        invalid_text = (
            "कृपया सही 10 अंकों का मोबाइल नंबर दर्ज करें (उदा. 9876543210):👇"
        )
        await update.message.reply_text(invalid_text)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("OlaPromo_bot is live!")
    app.run_polling()


if __name__ == "__main__":
    main()
