import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not BOT_TOKEN or not YOUTUBE_API_KEY:
    raise RuntimeError("Environment variables not set")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🎬 أرسل اسم الفيديو للبحث في يوتيوب")

@bot.message_handler(func=lambda m: True)
def search(msg):
    q = msg.text
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": q,
        "key": YOUTUBE_API_KEY,
        "maxResults": 1,
        "type": "video"
    }

    r = requests.get(url, params=params).json()

    if "items" not in r or not r["items"]:
        bot.reply_to(msg, "❌ لا توجد نتائج")
        return

    vid = r["items"][0]["id"]["videoId"]
    bot.reply_to(msg, f"https://youtu.be/{vid}")

@app.route("/", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.json)
    bot.process_new_updates([update])
    return "ok", 200
