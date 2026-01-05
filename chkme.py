import telebot, os, json, requests, random, string
from telebot import types
from datetime import datetime, timedelta

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
    id = str(message.from_user.id)
    with open('data.json', 'r') as f:
        try: data = json.load(f)
        except: data = {}
    
    plan = data.get(id, {}).get('plan', '𝗙𝗥𝗘𝗘')
    photo_url = 'https://t.me/hamk0oo/29'
    caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {message.from_user.first_name}\nPlan: {plan}\nCommands: /cmds</b>"
    bot.send_photo(message.chat.id, photo=photo_url, caption=caption)

# --- فەرمانا دروستکرنا کلیلان ---
@bot.message_handler(commands=["code"])
def create_code(message):
    if message.from_user.id != admin: return
    try:
        h = float(message.text.split(' ')[1])
        key = 'NEJA79-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        expire = (datetime.now() + timedelta(hours=h)).strftime("%Y-%m-%d %H:%M")
        
        with open('data.json', 'r') as f: data = json.load(f)
        data[key] = {"plan": "𝗩𝗜𝗣", "time": expire}
        with open('data.json', 'w') as f: json.dump(data, f, indent=4)
        
        bot.reply_to(message, f"<b>Key:</b> <code>/redeem {key}</code>")
    except: bot.reply_to(message, "Usage: /code 24")

# --- فەرمانا ئەکتیڤکرنێ ---
@bot.message_handler(func=lambda m: m.text.startswith(('/redeem', '.redeem')))
def redeem(message):
    try:
        key = message.text.split(' ')[1]
        with open('data.json', 'r') as f: data = json.load(f)
        if key in data:
            data[str(message.from_user.id)] = {"plan": "𝗩𝗜𝗣", "timer": data[key]['time']}
            del data[key]
            with open('data.json', 'w') as f: json.dump(data, f, indent=4)
            bot.reply_to(message, "<b>VIP Activated! ✅</b>")
        else: bot.reply_to(message, "Invalid Key!")
    except: bot.reply_to(message, "Usage: /redeem KEY")

print("Bot is Starting...")
bot.infinity_polling()
