import telebot, os, re, json, requests, time, random, string, threading
from telebot import types
from datetime import datetime, timedelta

# --- زانیاریێن بۆتی ---
token = '8243541935:AAGZ8VXWP-NB8c16rZHrd4ZLYDPG2u15Rpc' 
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 6421172039  # دڵنیابە ئەڤە ID یا تەیا دروستە

# --- هاوردەکرنا گەیتان (ئەگەر فایل نەبیت بۆت نامریت) ---
try:
    from gatet import *
except ImportError:
    pass

# --- فەرمانا Start ---
@bot.message_handler(commands=["start"])
def start(message):
    id = message.from_user.id
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as f: json.dump({}, f)
    
    with open('data.json', 'r') as f:
        try:
            data = json.load(f)
        except:
            data = {}
    
    plan = data.get(str(id), {}).get('plan', '𝗙𝗥𝗘𝗘')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="✨ 𝗢𝗪𝗡𝗘𝗥 ✨", url="https://t.me/d_7amko"))
    
    photo_url = 'https://t.me/hamk0oo/29'
    caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {message.from_user.first_name}\nPlan: {plan}\nCommands: /cmds</b>"
    bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=keyboard)

# --- فەرمانا دروستکرنا کلیلان (تنێ ئەدمین) ---
@bot.message_handler(commands=["code"])
def create_code(message):
    if message.from_user.id != admin:
        return
    try:
        h = float(message.text.split(' ')[1])
        chars = string.ascii_uppercase + string.digits
        key = 'NEJA79-' + '-'.join(''.join(random.choices(chars, k=4)) for _ in range(3))
        expire = (datetime.now() + timedelta(hours=h)).strftime("%Y-%m-%d %H:%M")
        
        with open('data.json', 'r') as f: data = json.load(f)
        data[key] = {"plan": "𝗩𝗜𝗣", "time": expire}
        with open('data.json', 'w') as f: json.dump(data, f, indent=4)
        
        bot.reply_to(message, f"<b>Key:</b> <code>/redeem {key}</code>\n<b>Hours: {h}</b>")
    except:
        bot.reply_to(message, "Usage: /code 24")

# --- فەرمانا ئەکتیڤکرنێ ---
@bot.message_handler(func=lambda m: m.text.startswith(('/redeem', '.redeem')))
def redeem(message):
    try:
        key = message.text.split(' ')[1]
        with open('data.json', 'r') as f: data = json.load(f)
        if key in data and "plan" in data[key]:
            data[str(message.from_user.id)] = {"plan": "𝗩𝗜𝗣", "timer": data[key].get('time', 'none')}
            del data[key]
            with open('data.json', 'w') as f: json.dump(data, f, indent=4)
            bot.reply_to(message, "<b>VIP Activated! ✅</b>")
        else:
            bot.reply_to(message, "Invalid Key!")
    except:
        bot.reply_to(message, "Usage: /redeem KEY")

print("Bot is working...")
bot.infinity_polling()
