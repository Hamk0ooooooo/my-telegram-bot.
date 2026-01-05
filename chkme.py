import telebot, os, re, json, requests, time, random, string, threading
from telebot import types
from datetime import datetime, timedelta

# --- زانیاریێن بۆتی ---
token = '8243541935:AAGZ8VXWP-NB8c16rZHrd4ZLYDPG2u15Rpc' 
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 8489120397 

# --- هاوردەکرنا فەحسکرنێ ژ gatet ---
try:
    from gatet import *
except ImportError:
    pass

stopuser = {}

# --- دەستپێکا بۆتی ---
@bot.message_handler(commands=["start"])
def start(message):
    id = message.from_user.id
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as f: json.dump({}, f)
    
    with open('data.json', 'r') as f:
        data = json.load(f)
    
    plan = data.get(str(id), {}).get('plan', '𝗙𝗥𝗘𝗘')
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="✨ 𝗢𝗪𝗡𝗘𝗥 ✨", url="https://t.me/d_7amko"))
    
    photo_url = 'https://t.me/hamk0oo/29'
    caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {message.from_user.first_name}\nPlan: {plan}\nCommands: /cmds</b>"
    bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=keyboard)

# --- لیستا فەرمانان ---
@bot.message_handler(commands=["cmds"])
def cmds(message):
    id = message.from_user.id
    with open('data.json', 'r') as f: data = json.load(f)
    plan = data.get(str(id), {}).get('plan', '𝗙𝗥𝗘𝗘')
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f"Status: {plan}", callback_data='plan'))
    
    text = "<b>𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗟𝗶𝘀𝘁:\n\n✅ Shopify Charge\n✅ Braintree Auth\n\nSend .txt file to start.</b>"
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

# --- دروستکرنا کلیلان (Admin Only) ---
@bot.message_handler(commands=["code"])
def create_code(message):
    if message.from_user.id != admin: return
    try:
        h = float(message.text.split(' ')[1])
        key = 'NEJA79-' + '-'.join(''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3))
        expire = (datetime.now() + timedelta(hours=h)).strftime("%Y-%m-%d %H:%M")
        
        with open('data.json', 'r') as f: data = json.load(f)
        data[key] = {"plan": "𝗩𝗜𝗣", "time": expire}
        with open('data.json', 'w') as f: json.dump(data, f, indent=4)
        
        bot.reply_to(message, f"<b>Key:</b> <code>/redeem {key}</code>\n<b>Hours: {h}</b>")
    except:
        bot.reply_to(message, "Use: /code 24")

# --- ئەکتیڤکرنا کلیلێ ---
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
    except: bot.reply_to(message, "Use: /redeem KEY")

# --- فەحسکرنا فایلان ---
@bot.message_handler(content_types=["document"])
def handle_docs(message):
    id = message.from_user.id
    with open('data.json', 'r') as f: data = json.load(f)
    if data.get(str(id), {}).get('plan') != '𝗩𝗜𝗣':
        bot.reply_to(message, "Buy VIP first!")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    with open("combo.txt", "wb") as f: f.write(downloaded)
    
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Shopify", callback_data='b6'), types.InlineKeyboardButton("Braintree", callback_data='b7'))
    bot.reply_to(message, "Select Gateway:", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data in ['b6', 'b7'])
def run_checker(call):
    # ل ڤێرێ بۆت دێ فایلا gatet.py بکار ئینیت بۆ فەحسکرنێ
    bot.answer_callback_query(call.id, "Starting Check...")
    bot.edit_message_text("<b>Checker is running... 🚀</b>", call.message.chat.id, call.message.message_id)

print("Bot is working...")
bot.infinity_polling()
