import telebot, os, re, json, requests, time, random, string, threading
from telebot import types
from datetime import datetime, timedelta

# ئەگەر ئەڤ فایلە (gatet) ل دەف تە هەبیت دێ کار کەت
try:
    from gatet import *
except ImportError:
    pass

stopuser = {}
token = '8243541935:AAG2BVXMP-N88c16rZHrO4zLYDPC2uI5Rpc'
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 6421172099

@bot.message_handler(commands=["start"])
def start(message):
    id = message.from_user.id
    # دروستکرن یان خویندنا فایلا داتا
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as f: json.dump({}, f)
    
    with open('data.json', 'r') as file:
        try:
            json_data = json.load(file)
        except:
            json_data = {}
    
    BL = json_data.get(str(id), {}).get('plan', '𝗙𝗥𝗘𝗘')
    keyboard = types.InlineKeyboardMarkup()
    contact_button = types.InlineKeyboardButton(text="✨ OWNER ✨", url="https://t.me/d_7amko")
    keyboard.add(contact_button)

    photo_url = 'https://t.me/hamk0oo/29'
    if BL == '𝗙𝗥𝗘𝗘':
        caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {message.from_user.first_name}\nYour Plan: {BL}\nTo purchase VIP: @d_7amko</b>"
    else:
        caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {message.from_user.first_name}\nYour Plan: {BL}\nSend .txt file to start checking!</b>"
    
    bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=keyboard)

@bot.message_handler(commands=["stop"])
def stop_checking(message):
    stopuser[message.from_user.id] = True
    bot.reply_to(message, "<b>Stopping soon... 🛑</b>")

@bot.message_handler(content_types=["document"])
def document_handler(message):
    id = message.from_user.id
    # پشکنینا پلانا VIP
    with open('data.json', 'r') as file:
        data = json.load(file)
    if data.get(str(id), {}).get('plan') != '𝗩𝗜𝗣' and id != admin:
        bot.reply_to(message, "<b>Buy VIP to use the checker! ❌</b>")
        return

    # وەرگرتنا فایلێ
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("combo.txt", "wb") as f:
        f.write(downloaded_file)
    
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Shopify Charge 💳", callback_data='shopify')
    btn2 = types.InlineKeyboardButton("Braintree Auth 🔐", callback_data='braintree')
    keyboard.add(btn1, btn2)
    
    bot.reply_to(message, "<b>Select Gateway to start:</b>", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['shopify', 'braintree'])
def start_checking(call):
    id = call.from_user.id
    stopuser[id] = False
    
    with open("combo.txt", "r") as f:
        lines = f.readlines()
    
    total = len(lines)
    msg = bot.send_message(call.message.chat.id, f"<b>Processing: 0/{total}</b>")
    
    live = 0
    dead = 0
    
    for line in lines:
        if stopuser.get(id): break
        
        card = line.strip()
        # ل ڤێرێ بانگکرنا فەنکشنا فەحسکرنێ ژ گەیتێ تە (Tele, Shopify, هتد)
        # ئەڤە نموونەیە، دڤێت ناڤێ فەنکشنێ ژ gatet.py بزانی
        try:
            # وەک نموونە: result = Tele(card)
            # دێ ل ڤێرێ ئەنجام هێتە پۆستکرن
            pass 
        except:
            pass
        
        # ل ڤێرێ هەر کارتەکا لایڤ (Live) بۆت دێ بۆ تە فرێکەت
        # bot.send_message(call.message.chat.id, f"✅ LIVE: {card}")
        
    bot.edit_message_text(f"<b>Check Completed! ✅\nTotal: {total}</b>", call.message.chat.id, msg.message_id)

@bot.message_handler(commands=['code'])
def make_key(message):
    if message.from_user.id == admin:
        try:
            days = message.text.split()[1]
            key = "NEJA-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
            # ل ڤێرێ پاشکەفت دناڤ داتا دا
            bot.reply_to(message, f"<b>Key Created:</b> <code>/redeem {key}</code>\n<b>Days: {days}</b>")
        except:
            bot.reply_to(message, "Use: /code 30")

print("Bot is working... ✅")
bot.infinity_polling()
