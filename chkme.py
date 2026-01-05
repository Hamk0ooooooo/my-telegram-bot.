import telebot, os, json, threading, random, string
from telebot import types
from datetime import datetime, timedelta
from gatet import ShopProcessor
from reg import reg

# --- زانیاریێن بۆتی ---
token = '8243541935:AAG2BVXMP-N88c16rZHrO4zLYDPC2uI5Rpc' 
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 6421172099 

# دروستکرنا فایلا داتا ئەگەر نەبیت
if not os.path.exists('data.json'):
    with open('data.json', 'w') as f: json.dump({}, f)

@bot.message_handler(commands=["start"])
def start(message):
    id = str(message.from_user.id)
    with open('data.json', 'r') as f:
        try: data = json.load(f)
        except: data = {}
    
    plan = data.get(id, {}).get('plan', '𝗙𝗥𝗘𝗘')
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="✨ OWNER ✨", url="https://t.me/d_7amko"))
    bot.send_photo(message.chat.id, photo='https://t.me/hamk0oo/29', 
                  caption=f"<b>𝑯𝑬𝑳𝑳𝑶 {message.from_user.first_name}\nPlan: {plan}\nSend .txt file to check!</b>", reply_markup=kb)

@bot.message_handler(content_types=["document"])
def handle_file(message):
    id = str(message.from_user.id)
    with open('data.json', 'r') as f: data = json.load(f)
    if data.get(id, {}).get('plan') != '𝗩𝗜𝗣' and message.from_user.id != admin:
        bot.reply_to(message, "<b>Buy VIP to use the checker! ❌</b>")
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    with open("combo.txt", "wb") as f: f.write(downloaded)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Shopify Auto 💳", callback_data='run_chk'))
    bot.reply_to(message, "<b>Choose Gateway:</b>", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data == 'run_chk')
def start_checking(call):
    bot.edit_message_text("<b>Starting Shopify Check... 🚀</b>", call.message.chat.id, call.message.message_id)
    with open("combo.txt", "r") as f: cards = f.readlines()
    
    # دروستکرنا دانەیا فەحسکرنێ ژ گەیتێ تە
    checker = ShopProcessor()
    
    for card in cards:
        card = card.strip()
        formatted_card = reg(card) # بەکارهێنانی فایلی reg.py بۆ ڕێکخستنی کارتەکە
        if not formatted_card: continue
        
        try:
            # بانگکرنا فەنکشنا فەحسکرنێ
            result = checker.execute(formatted_card) 
            if any(x in result for x in ["Approved", "CVV", "CCN", "1000"]):
                bot.send_message(call.message.chat.id, f"<b>✅ HIT: <code>{formatted_card}</code>\nResult: {result}</b>")
        except: continue
    
    bot.send_message(call.message.chat.id, "<b>Checking Finished! ✅</b>")

@bot.message_handler(commands=["code"])
def create_code(message):
    if message.from_user.id != admin: return
    try:
        h = int(message.text.split()[1])
        key = "NEJA-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        expire = (datetime.now() + timedelta(hours=h)).strftime("%Y-%m-%d %H:%M")
        with open('data.json', 'r') as f: data = json.load(f)
        data[key] = {"plan": "𝗩𝗜𝗣", "time": expire}
        with open('data.json', 'w') as f: json.dump(data, f, indent=4)
        bot.reply_to(message, f"<b>Key:</b> <code>/redeem {key}</code>")
    except: bot.reply_to(message, "Use: /code 24")

@bot.message_handler(func=lambda m: m.text and m.text.startswith('/redeem'))
def redeem(message):
    id = str(message.from_user.id)
    try:
        key = message.text.split()[1]
        with open('data.json', 'r') as f: data = json.load(f)
        if key in data:
            data[id] = {"plan": "𝗩𝗜𝗣", "timer": data[key]['time']}
            del data[key]
            with open('data.json', 'w') as f: json.dump(data, f, indent=4)
            bot.reply_to(message, "<b>VIP Activated! ✅</b>")
    except: pass

bot.infinity_polling()
