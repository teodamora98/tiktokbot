import telebot
import os
from dotenv import load_dotenv
import yt_dlp

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.chat.id != ALLOWED_USER_ID:
        bot.send_message(message.chat.id, "❌ Kamu tidak diizinkan menggunakan bot ini.")
        return

    url = message.text.strip()
    if "tiktok.com" not in url:
        bot.send_message(message.chat.id, "⚠️ Link tidak valid.")
        return

    bot.send_message(message.chat.id, "⏳ Mengunduh video...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'mp4',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        with open(video_path, 'rb') as f:
            bot.send_video(message.chat.id, f)
        os.remove(video_path)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Gagal: {e}")

print("🤖 Bot sedang berjalan...")
bot.polling()
