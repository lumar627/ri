from telegram.ext import Updater, CommandHandler
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
import yt_dlp
import os

BOT_TOKEN = '7532668167:AAEBb04qKyLCeFXW9sKOW_yfzmsbfuOU3j8'  # 🔑 Paste your Telegram bot token here

# Create downloads folder if not exist
os.makedirs("downloads", exist_ok=True)

def start(update: Update, context: CallbackContext):
    welcome_msg = (
        "👋 *Welcome to the Ultimate Video Downloader Bot!*\n\n"
        "⚡ Use the command like this:\n"
        "`/download insta <link>`\n"
        "`/download twitter <link>`\n"
        "`/download fb <link>`\n\n"
        "🎥 _Get videos directly from your favorite platforms!_\n\nBY :- @VILAXLORD 😎"
    )
    update.message.reply_text(welcome_msg, parse_mode='Markdown')

def download_video(link):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'http_headers': {'User-Agent': 'Mozilla/5.0'},
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        return ydl.prepare_filename(info)

def download_command(update: Update, context: CallbackContext):
    args = context.args

    if len(args) < 2:
        update.message.reply_text(
            "⚠️ *Invalid format!*\n\n"
            "Use like: `/download insta <link>`\n"
            "Use like: `/download twitter <link>`\n"
            "Use like: `/download fb <link>`",
            parse_mode='Markdown'
        )
        return

    platform = args[0].lower()
    link = args[1]

    update.message.reply_text(f"⏳ *Downloading from {platform.capitalize()}...*\nPlease wait a moment.", parse_mode='Markdown')

    try:
        filepath = download_video(link)
        if os.path.getsize(filepath) <= 49 * 1024 * 1024:
            with open(filepath, 'rb') as f:
                update.message.reply_video(f, caption=f"✅ Here's your *{platform}* video!", parse_mode='Markdown')
        else:
            update.message.reply_text("⚠️ *Video is too large for Telegram!*\nBut it was downloaded successfully.", parse_mode='Markdown')
    except Exception as e:
        update.message.reply_text(f"❌ *Error:* `{str(e)}`", parse_mode='Markdown')

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("download", download_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    