import telebot, os, json, requests
from telebot import types

# --- زانیاریێن بۆتی ---
token = '8243541935:AAGZ8VXWP-NB8c16rZHrd4ZLYDPG2u15Rpc' 
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 6421172039  # دڵنیابە ئەڤە ID یا تەیا دروستە

# --- دروستکرنا فایلا داتا ئەگەر نەبیت ---
if not os.path.exists('data.json'):
    with open('data.json', 'w') as f: json.dump({}, f)

# --- فەرمانا Start ---
@bot.message_handler(commands=["start"])
def start(message):
    photo_url = 'https://t.me/hamk0oo/29'
    caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {message.from_user.first_name}\nBot is Online ✅\nCommands: /cmds</b>"
    try:
        bot.send_photo(message.chat.id, photo=photo_url, caption=caption)
    except:
        bot.reply_to(message, caption)

# --- فەرمانا دروستکرنا کلیلان (تنێ ئەدمین) ---
@bot.message_handler(commands=["code"])
def create_code(message):
    if message.from_user.id != admin: return
    bot.reply_to(message, "<b>کلیل هاتە دروستکرن (نموونە)</b>")

print("Bot is Starting...")
bot.infinity_polling()
