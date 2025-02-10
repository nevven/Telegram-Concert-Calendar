# Standard library imports
from dotenv import load_dotenv
import os
import json
import logging
from datetime import datetime
from telegram.ext import Application, CommandHandler

# At the start of bot.py
if os.getenv('ENVIRONMENT') == 'production':
    # AWS: Use system logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
else:
    # Local: Use file logging
    logging.basicConfig(
        level=logging.INFO,
        filename='bot.log',
        format='%(asctime)s - %(message)s'
    )

logger = logging.getLogger(__name__)  # Create a logger instance

# Load environment variables from .env file
load_dotenv()

def load_data():
    """
    Load data from JSON file. Works both locally and on AWS
    """
    # Try AWS path first (flat structure)
    json_path = os.path.join('data', 'data.json')

    # If file not found, try local development path
    if not os.path.exists(json_path):
        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'data.json')
    
    try:
        # Try to read existing data
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except FileNotFoundError:
        logger.error(f"Data file not found at {json_path}")
        return {"concerts": [], "albums": []}


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
        "/koncerti - Raspored Koncerata\n"
        "/albumi - Nadolazeći Albumi"
    )
    await update.message.reply_text(help_text)

async def list_concerts(update, context):
    """
    Handler for /koncerti command
    Shows all upcoming concerts, sorted by date
    """
    try:
        data = load_data()
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
        message = "Evo, da ne zaboravite ;)\n\n\n`🎸    Koncerti    🎸`\n\n"
        for concert in upcoming:
            message += f"`{concert['band']}`\n"
            message += f"`{concert['date']} u {concert['time']}`\n"
            message += f"`{concert['venue']}, {concert['city']}`\n"
            message += f"`Karta: {concert['ticket']}`\n"
            message += f"{concert['link']}\n"  # No backticks for link
            message += f"───────────────────────\n\n"

        message += "\n🤘🏿"

        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"User {update.effective_user.username} requested concert list")
    
    except Exception as e:
        # Basic error handling - logs the error and notifies user
        logger.error(f"Error in list_concerts: {str(e)}")
        await update.message.reply_text("Sorry, nemogu dohvatit raspored")

async def list_albums(update, context):
    """
    Handler for /albumi command
    Shows all upcoming album releases, sorted by date
    """
    try:
        data = load_data()
        if not data.get('albums'):
            await update.message.reply_text("Nema albuma u bazi!")
            return

        # Sort albums by date
        today = datetime.now().date()
        upcoming = []
        
        for album in data.get('albums', []):
            album_date = datetime.strptime(album['date'], '%Y-%m-%d').date()
            if album_date >= today:
                upcoming.append(album)
        
        if not upcoming:
            await update.message.reply_text("Ne izlazi niš, uljenile se guzice, il me neven zaboravio nahranit s podacima")
            return

        # Sort by date
        upcoming.sort(key=lambda x: x['date'])
        
        # Format message
        message = "Evo, da i ovo ne zaboravite ;)\n\n\n`⚡    Albumi    ⚡`\n\n"
        for album in upcoming:
            message += f"`{album['band']}`\n"
            message += f"`{album['album']}`\n"
            message += f"`Izlazi: {album['date']}`\n"
            message += f"`Label: {album['label']}`\n"
            message += f"───────────────────────\n\n"

        message += "\n🤘🏿"

        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"User {update.effective_user.username} requested album list")
    
    except Exception as e:
        logger.error(f"Error in list_albums: {str(e)}")
        await update.message.reply_text("Sorry, nemogu dohvatit albume")

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
        app.add_handler(CommandHandler("albumi", list_albums))
        
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