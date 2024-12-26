
import telebot
import requests
import os

# Replace with your Telegram bot token
BOT_TOKEN = "7287522728:AAEXZpD60rOFCJFv28yyAgBxLUkYNJoK9fM"
bot = telebot.TeleBot(BOT_TOKEN)

# Directory to save downloaded files
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Welcome! Send me a link to a file or video, and I'll download it for you."
    )

@bot.message_handler(func=lambda message: message.text and message.text.startswith("http"))
def download_file(message):
    url = message.text.strip()
    bot.reply_to(message, "Downloading... Please wait.")
    
    try:
        # Send GET request to download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request is successful

        # Extract filename from URL or set a default
        filename = os.path.basename(url.split("?")[0]) or "downloaded_file"
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        
        # Save the file locally
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        # Upload the file to Telegram
        with open(file_path, "rb") as file:
            bot.send_document(message.chat.id, file)

        # Confirmation message
        bot.reply_to(message, f"Downloaded and sent: {filename}")
    
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Failed to download the file. Error: {e}")
    except Exception as e:
        bot.reply_to(message, f"An unexpected error occurred: {e}")

# Start the bot
print("Bot is running...")
bot.polling()
