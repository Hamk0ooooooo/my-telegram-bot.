import telebot, os, json, requests, threading, random, string
from telebot import types

# --- زانیاریێن بۆتی ---
token = '8243541935:AAG2BVXMP-N88c16rZHrO4zLYDPC2uI5Rpc' 
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 6421172099 

# هەوڵدان بۆ هاوردەکرنا گەیتێ ژ gatet.py
try:
    from gatet import Tele 
except:
    def Tele(card): return "Error: gatet.py function not found"

# دروستکرنا فایلا داتا ئەگەر نەبیت
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
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="✨ OWNER ✨", url="https://t.me/d_7amko"))
    
    photo_url = 'https://t.me/hamk0oo/29'
    caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {message.from_user.first_name}\nPlan: {plan}\nSend .txt file to check!</b>"
    bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=kb)

# --- وەرگرتنا فایلێ ---
@bot.message_handler(content_types=["document"])
def handle_file(message):
    id = str(message.from_user.id)
    with open('data.json', 'r') as f:
        data = json.load(f)
    
    if data.get(id, {}).get('plan') != '𝗩𝗜𝗣' and message.from_user.id != admin:
        bot.reply_to(message, "<b>Buy VIP to use the checker! ❌</b>")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    with open("combo.txt", "wb") as f: f.write(downloaded)
    
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Shopify Auto 💳", callback_data='run_chk'))
    bot.reply_to(message, "<b>Choose The Gateway To Use:</b>", reply_markup=kb)

# --- پرۆسەیا فەحسکرنێ ---
@bot.callback_query_handler(func=lambda call: call.data == 'run_chk')
def start_checking(call):
    bot.edit_message_text("<b>Starting Check... 🚀</b>", call.message.chat.id, call.message.message_id)
    
    with open("combo.txt", "r") as f:
        cards = f.readlines()
    
    for card in cards:
        card = card.strip()
        if not card: continue
        
        # ل ڤێرێ فایلا gatet.py دهێتە بکارئینان
        result = Tele(card) 
        
        if "Approved" in result or "CVV" in result or "CCN" in result:
            bot.send_message(call.message.chat.id, f"<b>✅ HIT: {card}\nResult: {result}</b>")
    
    bot.send_message(call.message.chat.id, "<b>Checking Finished! ✅</b>")

# --- فەرمانا دروستکرنا کلیلان ---
@bot.message_handler(commands=["code"])
def create_code(message):
    if message.from_user.id != admin: return
    try:
        h = message.text.split()[1]
        key = "NEJA-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        bot.reply_to(message, f"<b>Key:</b> <code>/redeem {key}</code>\n<b>Hours: {h}</b>")
    except: bot.reply_to(message, "Use: /code 24")

bot.infinity_polling()
