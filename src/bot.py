from dotenv import load_dotenv
import os
from telegram.ext import Application, CommandHandler

load_dotenv()

async def start(update, context):
    await update.message.reply_text("Hey! I'm your concert calendar bot!")

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("No token found! Check your .env file.")
    
    print("Bot is starting...")  # Debug message
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    main()