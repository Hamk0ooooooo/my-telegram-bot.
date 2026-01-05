import telebot, os
import re, json
import requests
import time, random
import string
from telebot import types
from datetime import datetime, timedelta
import threading

# --- ڕێکخستنا بۆتی ---
token = '8243541935:AAGZ8VXWP-NB8c16rZHrd4ZLYDPG2u15Rpc' 
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 8489120397 

# --- هاوردەکرنا گەیتان (دڵنیابە فایلا gatet.py ل دەف تە یا هەیە) ---
try:
    from gatet import *
except ImportError:
    print("Error: gatet.py not found!")

stopuser = {}

# --- فرمانێن سەرەکی ---
@bot.message_handler(commands=["start"])
def start(message):
    id = message.from_user.id
    name = message.from_user.first_name
    
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as f: json.dump({}, f)
            
    with open('data.json', 'r') as file:
        json_data = json.load(file)

    user_info = json_data.get(str(id), {"plan": "𝗙𝗥𝗘𝗘", "timer": "none"})
    plan = user_info.get('plan')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="✨ 𝗢𝗪𝗡𝗘𝗥 ✨", url="https://t.me/d_7amko"))
    
    photo_url = 'https://t.me/hamk0oo/29'
    
    if plan == '𝗙𝗥𝗘𝗘':
        caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {name}\nYour plan is FREE. Buy VIP to use checkers.\nContact: @d_7amko</b>"
    else:
        caption = f"<b>Welcome {name}!\nYour plan is {plan}.\nClick /cmds to see tools.</b>"
        
    bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=keyboard)

@bot.message_handler(commands=["cmds"])
def cmds(message):
    id = message.from_user.id
    with open('data.json', 'r') as file:
        json_data = json.load(file)
    
    plan = json_data.get(str(id), {}).get('plan', '𝗙𝗥𝗘𝗘')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f"✨ {plan} ✨", callback_data='plan'))
    
    text = "<b>𝗧𝗵𝗲𝘀𝗲 𝗔𝗿𝗲 𝗧𝗵𝗲 𝗕𝗼𝘁'𝗦 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n\n✅ SHOPIFY AUTO\n✅ BRAINTREE AUTH\n\nSend a .txt file to start checking!</b>"
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

# --- سیستەمێ کلیلان (Code & Redeem) ---
@bot.message_handler(commands=["code"])
def create_code(message):
    if message.from_user.id != admin: return
    try:
        h = float(message.text.split(' ')[1])
        chars = string.ascii_uppercase + string.digits
        key = 'NEJA79-' + '-'.join(''.join(random.choices(chars, k=4)) for _ in range(3))
        expire = (datetime.now() + timedelta(hours=h)).strftime("%Y-%m-%d %H:%M")
        
        with open('data.json', 'r') as f: data = json.load(f)
        data[key] = {"plan": "𝗩𝗜𝗣", "time": expire}
        with open('data.json', 'w') as f: json.dump(data, f, indent=4)
            
        bot.reply_to(message, f"<b>Key Created:</b>\n<code>/redeem {key}</code>\n<b>Expires in: {h} hours</b>")
    except:
        bot.reply_to(message, "<b>Usage: /code 24</b>")

@bot.message_handler(func=lambda m: m.text.startswith(('/redeem', '.redeem')))
def redeem(message):
    try:
        key = message.text.split(' ')[1]
        with open('data.json', 'r') as f: data = json.load(f)
        
        if key in data:
            data[str(message.from_user.id)] = {"plan": data[key]['plan'], "timer": data[key]['time']}
            del data[key]
            with open('data.json', 'w') as f: json.dump(data, f, indent=4)
            bot.reply_to(message, "<b>VIP Activated Successfully! ✅</b>")
        else:
            bot.reply_to(message, "<b>Invalid or Expired Key!</b>")
    except:
        bot.reply_to(message, "<b>Usage: /redeem KEY</b>")

# --- وەرگرتنا فایلێ کومبۆ ---
@bot.message_handler(content_types=["document"])
def handle_file(message):
    id = message.from_user.id
    with open('data.json', 'r') as f: data = json.load(f)
    
    if data.get(str(id), {}).get('plan') != '𝗩𝗜𝗣':
        bot.reply_to(message, "<b>Only VIP users can check files!</b>")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("combo.txt", "wb") as f: f.write(downloaded_file)
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Shopify Charge", callback_data='b6'))
    keyboard.add(types.InlineKeyboardButton("Braintree Auth", callback_data='b7'))
    bot.reply_to(message, "<b>File received! Choose a gateway:</b>", reply_markup=keyboard)

# --- تێبینی: ل ڤێرێ من بەشێ Callback یێ فەحسکرنێ کورت کر دا کۆد تێک نەچیت ---
# دڤێت فایلا gatet.py یا تەمام ل دەف تە هەبیت دا ڤی پشکی ب ڕێڤە ببەت.

@bot.callback_query_handler(func=lambda call: call.data in ['b6', 'b7'])
def start_checking(call):
    bot.edit_message_text("<b>Starting Check... ⌛</b>", call.message.chat.id, call.message.message_id)
    # ل ڤێرێ کۆدێ فەحسکرنێ یێ د ناڤ گەیتان دا دێ دەستپێکەت (وەک تە بەری نوکە پەیست کری)
    bot.send_message(call.message.chat.id, "<b>Checker is running in background...</b>")

print("Bot is Live ✅")
bot.infinity_polling()
