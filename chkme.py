import telebot, os
import re, json
import requests
import time, random
import string
from telebot import types
from datetime import datetime, timedelta
import threading

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
    def my_function():
        name = message.from_user.first_name
        id = message.from_user.id
        
        # دروستکرن یان خویندنا فایلا داتا
        try:
            with open('data.json', 'r') as file:
                json_data = json.load(file)
            BL = json_data.get(str(id), {}).get('plan', '𝗙𝗥𝗘𝗘')
        except:
            BL = '𝗙𝗥𝗘𝗘'
            if not os.path.exists('data.json'):
                with open('data.json', 'w') as f: json.dump({}, f)

        keyboard = types.InlineKeyboardMarkup()
        # ڕاستکرنا لینکێ OWNER
        contact_button = types.InlineKeyboardButton(text="✨ OWNER ✨", url="https://t.me/d_7amko")
        keyboard.add(contact_button)

        if BL == '𝗙𝗥𝗘𝗘':
            photo_url = 'https://t.me/hamk0oo/29'
            caption = f"<b>𝑯𝑬𝑳𝑳𝑶 {name}\nThe VIP plan allows you to use all tools...\nTo purchase: @d_7amko</b>"
            bot.send_photo(chat_id=message.chat.id, photo=photo_url, caption=caption, reply_markup=keyboard)
        else:
            photo_url = 'https://t.me/hamk0oo/29'
            bot.send_photo(chat_id=message.chat.id, photo=photo_url, caption="𝘾𝙡𝙞𝙘𝙠 /cmds 𝙏𝙤 𝙑𝙞𝙚𝙬 𝙏𝙝𝙚 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨", reply_markup=keyboard)

    threading.Thread(target=my_function).start()

@bot.message_handler(commands=["cmds"])
def cmds_handler(message):
    id = message.from_user.id
    try:
        with open('data.json', 'r') as file:
            json_data = json.load(file)
        BL = json_data.get(str(id), {}).get('plan', '𝗙𝗥𝗘𝗘')
    except:
        BL = '𝗙𝗥𝗘𝗘'
    
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text=f"✨ {BL} ✨", callback_data='plan')
    keyboard.add(btn)
    bot.send_message(chat_id=message.chat.id, text="<b>𝗧𝗵𝗲𝘀𝗲 𝗔𝗿𝗲 𝗧𝗵𝗲 𝗕𝗼𝘁'𝗦 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀\n✅ SHOPIFY AUTO\n✅ BRAINTREE AUTH</b>", reply_markup=keyboard)

@bot.message_handler(content_types=["document"])
def document_handler(message):
    id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    # ڕاستکرنا لینکێ OWNER ل ڤێرێ ژی
    contact_button = types.InlineKeyboardButton(text="✨ 𝗢𝗪𝗡𝗘𝗥 ✨", url="https://t.me/d_7amko")
    keyboard.add(contact_button)
    bot.reply_to(message, "𝘾𝙝𝙤𝙤𝙨𝙚 𝙏𝙝𝙚 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 𝙔𝙤𝙪 𝙒𝙖𝙣𝙩 𝙏𝙤 𝙐𝙨𝙚", reply_markup=keyboard)

# --- بەردەوامیا پشکێن دی یێن کۆدی وەک خۆ ---

print("Bot Start On ✅")
bot.infinity_polling()
