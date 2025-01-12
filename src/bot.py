# Standard library imports
from dotenv import load_dotenv
import os
import json
import logging
from datetime import datetime
from telegram.ext import Application, CommandHandler

# Set up basic logging - this will create a log file to help you track any issues
logging.basicConfig(
    level=logging.INFO,  # Logs info and errors
    filename='bot.log',  # All logs will go to this file
    format='%(asctime)s - %(message)s'  # Timestamp + message format
)
logger = logging.getLogger(__name__)  # Create a logger instance

# Load environment variables from .env file
load_dotenv()

def load_concerts():
    """
    Load concerts from JSON file. If file doesn't exist, create an empty one.
    In AWS, this file will be in the same directory as the bot script.
    """
    json_path = 'koncerti.json'  # Simplified path for AWS
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # If file doesn't exist, create a new one with empty concert list
        logger.info("Concert file not found, creating new one")
        data = {"concerts": []}
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return data

async def start(update, context):
    """Handler for /start command"""
    await update.message.reply_text(
        "Hey! I'm your concert calendar bot!\n"
        "Use /help to see what I can do!"
    )
    logger.info(f"User {update.effective_user.username} started the bot")  # Log who uses the bot

async def help(update, context):
    """Handler for /help command"""
    help_text = (
        "Available commands:\n\n"
        "/help - Show this help message\n"
        "/koncerti - Raspored Koncerata"
    )
    await update.message.reply_text(help_text)

async def list_concerts(update, context):
    """
    Handler for /list command
    Shows all upcoming concerts, sorted by date
    """
    try:
        data = load_concerts()
        if not data['concerts']:
            await update.message.reply_text("Nema koncerata u bazi!")
            return

        # Sort concerts by date
        today = datetime.now().date()
        upcoming = []
        
        for concert in data['concerts']:
            concert_date = datetime.strptime(concert['date'], '%Y-%m-%d').date()
            if concert_date >= today:
                upcoming.append(concert)
        
        if not upcoming:
            await update.message.reply_text("Nema koncerata na rasporedu :( ima koji za dodati?")
            return

        # Sort by date
        upcoming.sort(key=lambda x: x['date'])
        
        # Format message
        message = "Evo, da ne zaboravite ;) \n\n 🎸  Koncerti  🎸\n\n"
        for concert in upcoming:
            message += f"`{concert['band']}`\n"
            message += f"`{concert['date']} u {concert['time']}`\n"
            message += f"`{concert['venue']}`\n"
            message += f"`{concert['ticket']}`\n"
            message += f"{concert['link']}\n"
            message += f"──────────────\n"

        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"User {update.effective_user.username} requested concert list")
    
    except Exception as e:
        # Basic error handling - logs the error and notifies user
        logger.error(f"Error in list_concerts: {str(e)}")
        await update.message.reply_text("Sorry, nemogu dohvatit raspored")

async def error_handler(update, context):
    """
    Basic error handler - logs errors and sends a message to user
    """
    logger.error(f"Bot error: {context.error}")
    if update:
        await update.message.reply_text(
            "Sorry, nekaj se sj..., javi nevenu"
        )

def main():
    """
    Main function to run the bot
    """
    try:
        # Get bot token from environment variable
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            raise ValueError("No token found! Check your .env file.")
        
        # Create bot application
        logger.info("Bot is starting...")
        app = Application.builder().token(token).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help))
        app.add_handler(CommandHandler("koncerti", list_concerts))
        
        # Add error handler
        app.add_error_handler(error_handler)
        
        # Start the bot
        logger.info("Bot is ready to receive commands...")
        app.run_polling()

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise  # Re-raise the exception after logging it

if __name__ == '__main__':
    main()