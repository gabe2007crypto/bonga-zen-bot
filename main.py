import os
import time
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot

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

BOT_TOKEN = os.environ.get("BOT_TOKEN")
SOL_WALLET = os.environ.get("SOL_WALLET", "YOUR_SOL_WALLET_ADDRESS_HERE").strip()

bot = telebot.TeleBot(BOT_TOKEN)

VIBES = [
    "✌️ 'Peace comes from within. Do not seek it without.'",
    "🌸 'Keep your frequency high and your stress low.'",
    "🧘 'Inhale calm energy, exhale tension.'",
    "💚 'The pack moves together in peace and harmony.'",
    "✨ 'Chill out, hold strong, and raise the vibe.'"
]

# Reliable direct media URLs (Swap the GIF URL for your custom artwork!)
ZEN_AUDIO_URL = "https://actions.google.com/sounds/v1/water/waves_crashing_on_rock_beach.ogg" 
ZEN_ANIMATION_GIF = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3h0Y3h5am84aHhhcHgwdmVpZGpzZnFyeWJ3YmZ4ZzBveHZ5cHp1aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Lp8kVSaKEKVW8V7q8m/giphy.gif"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "✌️ **Welcome to Bonga Zen!** 🧘‍♂️\n\n"
        "Your personal space to breathe, relax, and keep your frequency high right here in chat.\n\n"
        "**Available Commands:**\n"
        "🟢 `/zen` or `/breathe` - Start 10-second animated breathing + ambient audio\n"
        "🌸 `/vibe` - Get a positive affirmation\n"
        "💚 `/tip` - Support the dev wallet"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['vibe'])
def send_vibe(message):
    quote = random.choice(VIBES)
    bot.reply_to(message, f"{quote}\n\n*✌️ Keep the vibes high!*", parse_mode="Markdown")

@bot.message_handler(commands=['zen', 'breathe'])
def start_zen(message):
    # 1. Send ambient audio with crash-protection
    try:
        bot.send_audio(
            message.chat.id, 
            ZEN_AUDIO_URL, 
            caption="🎧 *Playing Bonga Zen Ambient Soundscape...*", 
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Audio error: {e}")

    # 2. Send visual animation with crash-protection
    try:
        msg = bot.send_animation(
            message.chat.id,
            ZEN_ANIMATION_GIF,
            caption="🧘 **Starting Bonga Zen Session (10s intervals)...**",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Animation error: {e}")
        # Fallback to text if the image link ever fails
        msg = bot.send_message(
            message.chat.id, 
            "🧘 **Starting Bonga Zen Session...**", 
            parse_mode="Markdown"
        )
        
    time.sleep(2)

    # 10 seconds per phase
    phases = [
        ("🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n🌸 **Inhale deeply...** (10s)", 10),
        ("🟣🟣🟣🟣🟣🟣🟣🟣🟣🟣\n🧘 **Hold your breath...** (10s)", 10),
        ("🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦\n💨 **Exhale slowly...** (10s)", 10),
        ("🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨\n✌️ **Rest and hold...** (10s)", 10)
    ]

    for cycle in range(2):
        for text, duration in phases:
            try:
                # Check if we are editing a media caption or a plain text message
                if msg.content_type == 'animation':
                    bot.edit_message_caption(
                        chat_id=msg.chat.id,
                        message_id=msg.message_id,
                        caption=f"🧘 **Bonga Zen Breathing** (Cycle {cycle+1}/2)\n\n{text}",
                        parse_mode="Markdown"
                    )
                else:
                    bot.edit_message_text(
                        chat_id=msg.chat.id,
                        message_id=msg.message_id,
                        text=f"🧘 **Bonga Zen Breathing** (Cycle {cycle+1}/2)\n\n{text}",
                        parse_mode="Markdown"
                    )
            except Exception:
                pass
            time.sleep(duration)

    completion_text = (
        "🌟 **Zen Achieved!** 🌟\n\n"
        "You completed your breathing session and raised your frequency! ✌️💚\n\n"
        f"✌️ *Support the bot dev:* `{SOL_WALLET}`"
    )
    
    try:
        if msg.content_type == 'animation':
            bot.edit_message_caption(chat_id=msg.chat.id, message_id=msg.message_id, caption=completion_text, parse_mode="Markdown")
        else:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=completion_text, parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, completion_text, parse_mode="Markdown")

@bot.message_handler(commands=['tip', 'dev'])
def send_tip(message):
    tip_text = (
        "💚 **Support Bonga Zen Bot Dev** ✌️\n\n"
        "If this bot brought you peace, consider dropping a small tip to keep it running:\n\n"
        f"`{SOL_WALLET}`\n\n"
        "*(Click address above to copy)*"
    )
    bot.reply_to(message, tip_text, parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_http_server, daemon=True).start()
    print("Bonga Zen Bot is running live with Media! 🚀")
    
    # Adjusted polling to prevent sudden disconnects
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
