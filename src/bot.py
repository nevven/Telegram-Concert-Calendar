from dotenv import load_dotenv
import os
import json
from telegram.ext import Application, CommandHandler
from datetime import datetime

load_dotenv()

def load_concerts():
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'koncerti.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create empty concerts file if it doesn't exist
        data = {"concerts": []}
        os.makedirs(os.path.dirname(json_path), exist_ok=True)  # Create data directory if it doesn't exist
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return data

async def start(update, context):
    await update.message.reply_text(
        "Hey! I'm your concert calendar bot!\n"
        "Use /help to see what I can do!"
    )

async def help(update, context):
    help_text = (
        "Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/list - Show upcoming concerts"
    )
    await update.message.reply_text(help_text)

async def list_concerts(update, context):
    data = load_concerts()
    if not data['concerts']:
        await update.message.reply_text("No concerts scheduled!")
        return

    # Sort concerts by date
    today = datetime.now().date()
    upcoming = []
    
    for concert in data['concerts']:
        concert_date = datetime.strptime(concert['date'], '%Y-%m-%d').date()
        if concert_date >= today:
            upcoming.append(concert)
    
    if not upcoming:
        await update.message.reply_text("No upcoming concerts!")
        return

    # Sort by date
    upcoming.sort(key=lambda x: x['date'])
    
    # Format message
    message = "🎸 UPCOMING CONCERTS 🎸\n\n"
    for concert in upcoming:

        message += f"`{concert['band']}`\n"
        message += f"`{concert['date']} at {concert['time']}`\n"
        message += f"`{concert['venue']}`\n"
        message += f"`{concert['ticket']}`\n"
        message += f"{concert['link']}\n"
        message += f"──────────────\n"  # Divider line

    # Add parse_mode parameter here
    await update.message.reply_text(message, parse_mode='Markdown')

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("No token found! Check your .env file.")
    
    print("Bot is starting...")
    app = Application.builder().token(token).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("list", list_concerts))
    
    app.run_polling()

if __name__ == '__main__':
    main()