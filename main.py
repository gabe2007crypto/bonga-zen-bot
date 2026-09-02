import os
import time
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Dummy HTTP server so Render Web Service detects an open port immediately
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bonga Zen Bot is running live!")

def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Pull secrets safely from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SOL_WALLET = os.environ.get("SOL_WALLET", "YOUR_SOL_WALLET_ADDRESS_HERE").strip()
MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://preeminent-biscochitos-5bf4db.netlify.app").strip().strip('"').strip("'")

bot = telebot.TeleBot(BOT_TOKEN)

VIBES = [
    "✌️ 'Peace comes from within. Do not seek it without.'",
    "🌸 'Keep your frequency high and your stress low.'",
    "🧘 'Inhale green candles, exhale bad vibes.'",
    "💚 'The pack moves together in peace and harmony.'",
    "✨ 'Chill out, hold strong, and raise the vibe.'"
]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    app_btn = InlineKeyboardButton(
        text="🧘 Open Full Visual & Sound Experience ✌️", 
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    markup.add(app_btn)

    welcome_text = (
        "✌️ **Welcome to Bonga Zen!** 🧘‍♂️\n\n"
        "Your personal space to breathe, relax, and keep your frequency high.\n\n"
        "**Available Commands:**\n"
        "✨ `/app` - Launch full visual meditation space with audio\n"
        "🟢 `/zen` or `/breathe` - Start 2-cycle chat breathing (20s Inhale / 20s Hold)\n"
        "🌸 `/vibe` - Get a positive hippie affirmation\n"
        "💚 `/tip` - Support the dev wallet"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['app', 'meditate'])
def launch_mini_app(message):
    markup = InlineKeyboardMarkup()
    app_btn = InlineKeyboardButton(
        text="🧘 Tap to Start Visual Session ✌️", 
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    markup.add(app_btn)
    bot.reply_to(message, "Tap below to open your full visual breathing experience:", reply_markup=markup)

@bot.message_handler(commands=['vibe'])
def send_vibe(message):
    quote = random.choice(VIBES)
    bot.reply_to(message, f"{quote}\n\n*✌️ Keep the vibes high!*", parse_mode="Markdown")

@bot.message_handler(commands=['zen', 'breathe'])
def start_zen(message):
    msg = bot.reply_to(message, "🧘 **Starting Bonga Zen Session...**\nGet comfortable and clear your mind.", parse_mode="Markdown")
    time.sleep(2)

    phases = [
        ("🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n🌸 **Inhale deeply...** (20s)", 20),
        ("🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣\n🧘 **Hold your breath...** (20s)", 20),
        ("🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦\n💨 **Exhale slowly...** (20s)", 20),
        ("🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨\n✌️ **Rest and hold...** (20s)", 20)
    ]

    for cycle in range(2):
        for text, duration in phases:
            bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                text=f"🧘 **Bonga Zen Breathing** (Cycle {cycle+1}/2)\n\n{text}",
                parse_mode="Markdown"
            )
            time.sleep(duration)

    completion_text = (
        "🌟 **Zen Achieved!** 🌟\n\n"
        "You completed 2 deep breathing cycles and raised your frequency! ✌️💚\n\n"
        f"✌️ *Support the bot dev:* `{SOL_WALLET}`"
    )
    bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        text=completion_text,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['tip', 'dev'])
def send_tip(message):
    tip_text = (
        "💚 **Support Bonga Zen Bot Dev** ✌️\n\n"
        "If this bot brought you peace, consider dropping a small $BONGA or $SOL tip to keep it running:\n\n"
        f"`{SOL_WALLET}`\n\n"
        "*(Click address above to copy)*"
    )
    bot.reply_to(message, tip_text, parse_mode="Markdown")

if __name__ == "__main__":
    # Start the HTTP web server in the background so Render port check passes instantly
    threading.Thread(target=run_http_server, daemon=True).start()
    
    print("Bonga Zen Bot is running live! 🚀")
    bot.infinity_polling()
