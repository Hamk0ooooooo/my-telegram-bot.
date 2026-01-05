import telebot, os, json, threading, random, string
from telebot import types
from datetime import datetime, timedelta
from gatet import ShopProcessor # بانگکرنا گەیتێ تە
from reg import reg # بانگکرنا ڕێکخستنا کارتێ

# --- زانیاریێن بۆتی ---
token = '8243541935:AAG2BVXMP-N88c16rZHrO4zLYDPC2uI5Rpc' 
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 6421172099 

@bot.message_handler(commands=["start"])
def start(message):
    id = str(message.from_user.id)
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as f: json.dump({}, f)
    with open('data.json', 'r') as f: data = json.load(f)
    plan = data.get(id, {}).get('plan', '𝗙𝗥𝗘𝗘')
    bot.send_photo(message.chat.id, photo='https://t.me/hamk0oo/29', 
                  caption=f"<b>𝑯𝑬𝑳𝑳𝑶 {message.from_user.first_name}!\nPlan: {plan}\nSend .txt file to check!</b>")

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
    bot.reply_to(message, "<b>File Loaded! Click to start:</b>", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data == 'run_chk')
def start_checking(call):
    bot.edit_message_text("<b>Starting Shopify Check... 🚀</b>", call.message.chat.id, call.message.message_id)
    with open("combo.txt", "r") as f: cards = f.readlines()
    
    checker = ShopProcessor() # ئامادەکرنا گەیتێ
    
    for card in cards:
        card = card.strip()
        formatted_card = reg(card) # پاقژکرنا کارتێ
        if not formatted_card: continue
        
        try:
            # بکارئینانا فەنکشنا process_card کو د فایلا تە دا هەبوو
            result = checker.process_card(formatted_card) 
            if any(x in result for x in ["Approved", "CVV", "CCN", "1000"]):
                bot.send_message(call.message.chat.id, f"<b>✅ HIT: <code>{formatted_card}</code>\nResult: {result}</b>")
        except: continue
    bot.send_message(call.message.chat.id, "<b>Checking Finished! ✅</b>")

bot.infinity_polling()
