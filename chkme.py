import telebot, os, re, json, requests, time, random, string, threading
from telebot import types
from datetime import datetime, timedelta

# ئەگەر فایلا gatet یا هەبیت
try:
    from gatet import *
except:
    pass

token = '8243541935:AAG2BV/XMP-N88c16rZHrO4zLYDPC2uI5Rpc' # ل ڤێرێ تۆکنێ خۆ یێ نوو دانە ئەگەر کار نەکر
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 6421172099
stopuser = {}

@bot.message_handler(commands=["start"])
def start(message):
    def my_function():
        id = message.from_user.id
        name = message.from_user.first_name
        
        if not os.path.exists('data.json'):
            with open('data.json', 'w') as f: json.dump({}, f)
        
        with open('data.json', 'r') as file:
            data = json.load(file)
        
        if str(id) not in data:
            data[str(id)] = {"plan": "𝗙𝗥𝗘𝗘", "timer": "none"}
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
        
        plan = data[str(id)].get('plan', '𝗙𝗥𝗘𝗘')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="✨ OWNER ✨", url="https://t.me/d_7amko"))

        caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {name}\nPlan: {plan}\nTo purchase VIP: @d_7amko</b>"
        bot.send_photo(message.chat.id, photo='https://t.me/hamk0oo/29', caption=caption, reply_markup=keyboard)

    threading.Thread(target=my_function).start()

@bot.message_handler(commands=["cmds"])
def cmds(message):
    bot.reply_to(message, "<b>𝗧𝗵𝗲𝘀𝗲 𝗔𝗿𝗲 𝗧𝗵𝗲 𝗕𝗼𝘁'𝗦 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n\n✅ SHOPIFY AUTO\n✅ BRAINTREE AUTH</b>")

@bot.message_handler(content_types=["document"])
def handle_docs(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="SHOPIFY", callback_data='b6'),
                 types.InlineKeyboardButton(text="BRAINTREE", callback_data='b7'))
    bot.reply_to(message, "𝘾𝙝𝙤𝙤𝙨𝙚 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_call(call):
    stopuser[f"{call.from_user.id}"] = {'status': 'stop'}
    bot.answer_callback_query(call.id, "Stopped ✅")

print("Bot is running... ✅")
bot.infinity_polling()
