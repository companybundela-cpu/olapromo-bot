import html
import logging
import os
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dummy Health Check Server for Render Port Scan
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    logger.info(f"Health check server running on port {port}")
    server.serve_forever()

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
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()
    chat_id = update.effective_chat.id
    raw_username = update.effective_user.username or "No Username"
    raw_first_name = update.effective_user.first_name or "Gamer"

    # Escape special characters
    safe_name = html.escape(raw_first_name)
    safe_username = html.escape(raw_username)

    # Clean non-digits
    clean_number = re.sub(r'\D', '', user_text)

    # 10-digit check
    phone_pattern = r'^[6-9]\d{9}$'

    if re.match(phone_pattern, clean_number):
        keyboard = [
            [InlineKeyboardButton("🌐 Visit Website", url="https://bundela247.com/")],
            [InlineKeyboardButton("💬 Join WhatsApp Support", url="https://wa.me/message/UWIN3RSRLUJQE1")],
            [InlineKeyboardButton("📢 Join Telegram Channel", url="https://t.me/BUNDELA247")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        reply_text = (
            "🏆 <b>Welcome to BUNDELA247 VIP</b> 🏆\n"
            "India's Most Trusted & Premium Sports Community! ⚡\n\n"
            "✅ 24x7 Superfast VIP Service\n"
            "✅ 100% Safe & Secure Database\n\n"
            "धन्यवाद! 🎮 आपका नंबर दर्ज हो गया है। हमारी टीम जल्द ही आपसे संपर्क करेगी। 👍\n\n"
            "👇 <b>Get Your Premium VIP Access Now:</b>"
        )
        await update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode='HTML')

        # Admin alert
        admin_alert = (
            f"🚀 <b>NEW LEAD CAPTURED!</b>\n\n"
            f"👤 <b>Name:</b> {safe_name}\n"
            f"🆔 <b>Username:</b> @{safe_username}\n"
            f"📞 <b>Phone Number:</b> <code>{clean_number}</code>\n"
            f"💬 <b>Chat ID:</b> <code>{chat_id}</code>"
        )
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID, 
            text=admin_alert, 
            parse_mode='HTML'
        )
        
        logger.info(f"NEW LEAD CAPTURED: Chat ID: {chat_id} | Phone: {clean_number}")

    else:
        # Invalid format
        error_text = (
            "⚠️ <b>अमान्य मोबाइल नंबर!</b>\n\n"
            "कृपया सही 10 अंकों का मोबाइल नंबर दर्ज करें (उदा. 9876543210): 👇"
        )
        await update.message.reply_text(error_text, parse_mode='HTML')

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception handling update:", exc_info=context.error)

if __name__ == '__main__':
    # Start port binding server for Render in background thread
    threading.Thread(target=run_health_server, daemon=True).start()

    TOKEN = "8951896304:AAF8FGMhRKzmBVLmia7oLALvkEeVchsjtdY"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_error_handler(error_handler)

    print("Bot is running...")
    app.run_polling()
