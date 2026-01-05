import telebot, os, json, threading
from telebot import types
# هاوردەکردنی پۆلی فەحسکردن لە گەیتەکەت
try:
    from gatet import ShopProcessor
except ImportError:
    ShopProcessor = None

token = '8243541935:AAG2BVXMP-N88c16rZHrO4zLYDPC2uI5Rpc' 
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 6421172099 

@bot.callback_query_handler(func=lambda call: call.data == 'run_chk')
def start_checking(call):
    if not ShopProcessor:
        bot.answer_callback_query(call.id, "Error: ShopProcessor not found in gatet.py")
        return

    bot.edit_message_text("<b>Starting Shopify Check... 💳</b>", call.message.chat.id, call.message.message_id)
    
    # دەستپێکردنی پڕۆسێسەری گەیتەکە
    proc = ShopProcessor()
    
    try:
        with open("combo.txt", "r") as f:
            cards = f.readlines()
        
        for card in cards:
            card = card.strip()
            if not card: continue
            
            # لێرەدا فەنکشنی سەرەکی گەیتەکە بانگ دەکەین (بۆ نموونە execute یان process)
            # تێبینی: بەپێی وێنەکە دەبێت بزانی کام فەنکشن فەحسەکە دەکات
            try:
                # ئەگەر فەنکشنەکە ناوی execute بێت:
                # res = proc.execute(card) 
                bot.send_message(call.message.chat.id, f"<b>Checking:</b> <code>{card}</code>")
            except:
                continue
                
        bot.send_message(call.message.chat.id, "<b>Check Completed! ✅</b>")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error: {str(e)}")

bot.infinity_polling()
