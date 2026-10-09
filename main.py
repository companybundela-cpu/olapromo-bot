import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Admin Chat ID
ADMIN_CHAT_ID = 7926478504

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "नमस्ते गेमर! 🎰 हमारे साथ अपना गेमिं ग अकाउंट बनाने के लिए "
        "कृपया अपना 10 अंकों का मोबाइल नंबर यहाँ टाइप करके भेजें: 👇"
    )
    await update.message.reply_text(welcome_text)

# Phone number & message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    chat_id = update.effective_chat.id
    username = update.effective_user.username or "No Username"
    first_name = update.effective_user.first_name or ""

    # 10-digit phone number check (Regex)
    phone_pattern = r'^[6-9]\d{9}$'

    if re.match(phone_pattern, user_text):
        # Interactive Buttons (Inline Keyboard)
        keyboard = [
            [InlineKeyboardButton("🌐 Visit Website", url="https://bundela247.com/")],
            [InlineKeyboardButton("💬 Join WhatsApp Support", url="https://wa.me/message/UWIN3RSRLUJQE1")],
            [InlineKeyboardButton("📢 Join Telegram Channel", url="https://t.me/BUNDELA247")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # User ko reply with VIP Message & Buttons
        reply_text = (
            "🏆 **Welcome to BUNDELA247 VIP** 🏆\n"
            "India's Most Trusted & Premium Sports Community! ⚡\n\n"
            "✅ 24x7 Superfast VIP Service\n"
            "✅ 100% Safe & Secure Database\n\n"
            "धन्यवाद! 🎮 आपका नंबर दर्ज हो गया है। हमारी टीम जल्द ही आपसे संपर्क करेगी। 👍\n\n"
            "👇 **Get Your Premium VIP Access Now:**"
        )
        await update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode='Markdown')

        # Admin (Aapko) direct notification message
        admin_alert = (
            f"🚀 **NEW LEAD CAPTURED!**\n\n"
            f"👤 **Name:** {first_name}\n"
            f"🆔 **Username:** @{username}\n"
            f"📞 **Phone Number:** `{user_text}`\n"
            f"💬 **Chat ID:** `{chat_id}`"
        )
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID, 
            text=admin_alert, 
            parse_mode='Markdown'
        )
        
        logging.info(f"NEW LEAD CAPTURED: Chat ID: {chat_id} | Phone: {user_text}")

    else:
        # Invalid number format
        error_text = "कृपया सही 10 अंकों का मोबाइल नंबर दर्ज करें (उदा. 9876543210): 👇"
        await update.message.reply_text(error_text)

if __name__ == '__main__':
    # Naya Revoked Bot Token
    TOKEN = "8951896304:AAF8FGMhRKzmBVLmia7oLALvkEeVchsjtdY"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    app.run_polling()
