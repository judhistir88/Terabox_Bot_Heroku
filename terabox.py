import os
import re
import requests
import telebot
import logging
from time import time, sleep
import config
from flask import Flask, request, jsonify
from threading import Thread
import pymongo
import random
from progress_bars import get_random_progress_bar  # Import the random progress bar function

# Set up logging
logging.basicConfig(level=logging.INFO)
# DB Connetion

mongo_client = pymongo.MongoClient(config.MONGO_URL)
db = mongo_client['terabox_tg-bot']
users_collection = db['users']
banned_users_collection = db['banned_users']
print('DB Connected')

# Bot Connetion
bot = telebot.TeleBot(config.BOT_TOKEN)
print(f"@{bot.get_me().username} Connected")
print("\n╭─── [ LOG ]")
app = Flask(__name__)

# Webhook
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    bot.remove_webhook()  # Remove any existing webhook
    bot.set_webhook(url=os.getenv('WEBHOOK_URL'))  # Set the new webhook
    return "Webhook has been set", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_json())
    bot.process_new_updates([update])
    return 'ok', 200

# Functions
# Fetch User Member or Not
def is_member(user_id):
    try:
        member_status = bot.get_chat_member('-1001702284560', user_id)
        return member_status.status in ['member', 'administrator', 'creator']
    except:
        return False

# Function to format the progress bar
def format_progress_bar(filename, percentage, done, total_size, speed):
    bar_length = 10  # Set the bar length to 10
    bar_style = get_random_progress_bar()  # Get a random progress bar style
    filled_char = bar_style[0]
    empty_char = bar_style[1]
    filled_length = int(bar_length * (percentage // 10) / 10)  # Show progress in 10% increments
    bar = filled_char * filled_length + empty_char * (bar_length - filled_length)

    def format_size(size):
        size = int(size)
        if size < 1024:
            return f"{size} B"
        elif size < 1024 ** 2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024 ** 3:
            return f"{size / 1024 ** 2:.2f} MB"
        else:
            return f"{size / 1024 ** 3:.2f} GB"

    return (
        f"File: {filename}\n"
        f"[{bar}] {percentage:.2f}%\n"
        f"Processed: {format_size(done)} of {format_size(total_size)}\n"
        f"Speed: {format_size(speed)}/s"
    )

# Function to download video
def download_video(url, chat_id, message_id, user_mention, user_id):
    response = requests.get(f'https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url={url}')
    data = response.json()

    if not data['response'] or len(data['response']) == 0:
        raise Exception('No response data found')

    resolutions = data['response'][0]['resolutions']
    fast_download_link = resolutions['Fast Download']
    video_title = re.sub(r'[<>:"/\\|?*]+', '', data['response'][0]['title'])
    video_path = os.path.join('Videos', f"{video_title}.mp4")

    # Check the file size before downloading
    head_response = requests.head(fast_download_link)
    total_length = head_response.headers.get('content-length')
    if total_length is None:
        raise Exception('Could not determine the file size.')

    max_size = 1.5 * 1024 * 1024 * 1024  # 1.5 GB in bytes
    total_length = int(total_length)
    if total_length > max_size:
        raise Exception('The file size exceeds the maximum allowed size of 1.5 GB.')

    with open(video_path, 'wb') as video_file:
        video_response = requests.get(fast_download_link, stream=True)

        downloaded_length = 0
        start_time = time()
        last_update_time = start_time
        for chunk in video_response.iter_content(chunk_size=4096):
            downloaded_length += len(chunk)
            video_file.write(chunk)
            current_time = time()
            elapsed_time = current_time - start_time
            if current_time - last_update_time >= 5:
                percentage = 100 * downloaded_length / total_length
                speed = downloaded_length / elapsed_time

                progress = format_progress_bar(
                    video_title,
                    percentage,
                    downloaded_length,
                    total_length,
                    speed
                )
                bot.edit_message_text(progress, chat_id, message_id)
                last_update_time = current_time
    
    return video_path, video_title, total_length

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user = message.from_user

        bot.send_chat_action(message.chat.id, 'typing')

        # Store User To DB
        if not users_collection.find_one({'user_id': user.id}):
            users_collection.insert_one({
                'user_id': user.id,
                'first_name': user.first_name,
                'downloads': 0
            })

        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        inline_keyboard.row(
            telebot.types.InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url=f"https://t.me/MCS4U2")
        )

        bot.send_message(
            message.chat.id, 
            (
                f"ᴡᴇʟᴄᴏᴍᴇ, <a href='tg://user?id={user.id}'>{user.first_name}</a>.\n\n"
                "🌟 ɪ ᴀᴍ ᴀ ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ.\n"
                "sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ ɪ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ᴡɪᴛʜɪɴ ғᴇᴡ sᴇᴄᴏɴᴅs\n"
                "ᴀɴᴅ sᴇɴᴅ ɪᴛ ᴛᴏ ʏᴏᴜ ✨"
            ), 
            parse_mode='HTML', 
            reply_markup=inline_keyboard
        )
    except Exception as e:
        logging.error(f"Error in /start command: {e}")
        bot.send_message(message.chat.id, "An error occurred. Please try again later.")

# Ban command
@bot.message_handler(commands=['ban'])
def ban_user(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if str(message.from_user.id) != config.BOT_TOKEN:
        bot.reply_to(message, "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪꜱᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ")
        return

    if len(message.text.split()) < 2:
        bot.reply_to(message, "ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴜꜱᴇʀ ᴛᴏ ʙᴀɴ.")
        return

    user_id_to_ban = int(message.text.split()[1])

    if banned_users_collection.find_one({'user_id': user_id_to_ban}):
        bot.reply_to(message, f"ᴛʜɪꜱ ᴜꜱᴇʀ <code>{user_id_to_ban}</code> ɪꜱ ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ.", parse_mode='HTML')
        return

    banned_users_collection.insert_one({'user_id': user_id_to_ban})
    bot.reply_to(message, f"ᴛʜɪꜱ ᴜꜱᴇʀ <code>{user_id_to_ban}</code> ʜᴀꜱ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.", parse_mode='HTML')

# Unban command
@bot.message_handler(commands=['unban'])
def unban_user(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if str(message.from_user.id) != config.BOT_TOKEN:
        bot.reply_to(message, "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪꜱᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ")
        return

    if len(message.text.split()) < 2:
        bot.reply_to(message, "ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴜɴʙᴀɴ.")
        return

    user_id_to_unban = int(message.text.split()[1])

    if not banned_users_collection.find_one({'user_id': user_id_to_unban}):
        bot.reply_to(message, f"ᴛʜɪꜱ ᴜꜱᴇʀ <code>{user_id_to_unban}</code> ɪꜱ ɴᴏᴛ ᴄᴜʀʀᴇɴᴛʟʏ ʙᴀɴɴᴇᴅ.", parse_mode='HTML')
        return

    banned_users_collection.delete_one({'user_id': user_id_to_unban})
    bot.reply_to(message, f"ᴛʜɪꜱ ᴜꜱᴇʀ <code>{user_id_to_unban}</code> ʜᴀꜱ ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ.", parse_mode='HTML')

# Broadcast
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if str(message.from_user.id) != config.BOT_TOKEN:
        bot.reply_to(message, "You are not authorized to use this command.")
        return
    bot.reply_to(message, 'ᴘʀᴏᴠɪᴅᴇ ᴀ ᴍᴇꜱꜱᴀɢᴇ / ᴍᴇᴅɪᴀ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ', reply_markup=telebot.types.ForceReply(selective=True))
    bot.register_next_step_handler(message, process_broadcast_message)

def process_broadcast_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    total_users = len(get_user_ids()) - 1
    successful_users = 0
    blocked_users = 0
    deleted_accounts = 0
    unsuccessful_users = 0

    # Send the message to all users
    for broadcast_user_id in get_user_ids():
        if broadcast_user_id != user_id:
            try:
                if message.photo:
                    photo_id = message.photo.pop().file_id
                    caption = message.caption or ''
                    bot.send_photo(broadcast_user_id, photo_id, caption=caption, parse_mode='html')
                    successful_users += 1
                elif message.video:
                    video_id = message.video.file_id
                    caption = message.caption or ''
                    bot.send_video(broadcast_user_id, video_id, caption=caption, parse_mode='html')
                    successful_users += 1
                elif message.text:
                    text = message.text
                    bot.send_message(broadcast_user_id, text, parse_mode='html')
                    successful_users += 1
            except telebot.apihelper.ApiException as e:
                if e.error_code == 403:  # Forbidden (likely user blocked the bot)
                    blocked_users += 1
                elif e.error_code == 400 and 'user not found' in str(e):  # User not found (likely deleted account)
                    deleted_accounts += 1
                    users_collection.delete_one({'user_id': broadcast_user_id})
                else:
                    unsuccessful_users += 1
                    print(f"Error sending message to user {broadcast_user_id}: {e}")

    unsuccessful_users = total_users - successful_users - blocked_users - deleted_accounts
    bot.send_message(
        chat_id,
        f"""✅ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.\n
ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: <code>{total_users}</code>
ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful_users}</code>
ʙʟᴏᴄᴋᴇᴅ ᴜꜱᴇʀꜱ: <code>{blocked_users}</code>
ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ: <code>{deleted_accounts}</code>
ᴜɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful_users}</code>""",
        parse_mode='HTML'
    )

# Get User IDs
def get_user_ids():
    # Get user IDs from your database
    user_ids = [user['user_id'] for user in users_collection.find()]
    return user_ids

# Handle messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = message.from_user

    # Ignore
    if message.text.startswith('/'):
        return

    bot.send_chat_action(message.chat.id, 'typing')

    # Check if user is banned
    if banned_users_collection.find_one({'user_id': user.id}):
        bot.send_message(message.chat.id, "You are banned from using this bot contact Owner.")
        return

    # Check User Member or Not
    if not is_member(user.id):
        bot.send_message(
            message.chat.id,
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ.",
            reply_markup=telebot.types.InlineKeyboardMarkup().add(
                telebot.types.InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url=f"https://t.me/MCS4U2")
            )
        )
        return

    video_url = message.text
    chat_id = message.chat.id
    user_mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    user_id = user.id

    if re.match(r'http[s]?://.*tera', video_url):
        progress_msg = bot.send_message(chat_id, 'ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ᴠɪᴅᴇᴏ...')
        try:
            video_path, video_title, video_size = download_video(video_url, chat_id, progress_msg.message_id, user_mention, user_id)
            bot.edit_message_text('sᴇɴᴅɪɴɢ ʏᴏᴜ ᴛʜᴇ ᴍᴇᴅɪᴀ...🤤', chat_id, progress_msg.message_id)

            video_size_mb = video_size / (1024 * 1024)

            dump_channel_video = bot.send_video(os.getenv('DUMP_CHAT_ID'), open(video_path, 'rb'), caption=f"✨ {video_title}\n📀 {video_size_mb:.2f} MB\n👤 ʟᴇᴇᴄʜᴇᴅ ʙʏ : {user_mention}")
            bot.copy_message(chat_id, os.getenv('DUMP_CHAT_ID'), dump_channel_video.message_id)

            bot.send_sticker(chat_id, "CAACAgIAAxkBAAEZdwRmJhCNfFRnXwR_lVKU1L9F3qzbtAAC4gUAAj-VzApzZV-v3phk4DQE")
            users_collection.update_one(
                {'user_id': user.id},
                {'$inc': {'downloads': 1}},
                upsert=True
            )
            bot.delete_message(chat_id, progress_msg.message_id)
            bot.delete_message(chat_id, message.message_id)
            os.remove(video_path)
        except Exception as e:
            bot.edit_message_text(f'Download failed: {str(e)}', chat_id, progress_msg.message_id)
    else:
        bot.send_message(chat_id, 'ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ.')

# Home
@app.route('/')
def index():
    return 'Bot Is Alive'

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status='OK'), 200

if __name__ == "__main__":
    # Start Flask app in a separate thread
    def run_flask():
        app.run(host='0.0.0.0', port=config.PORT)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()
