#!/usr/bin/env python3
import json
import os
import asyncio
from datetime import datetime
from telegram import Bot

# Configuration
BOT_TOKEN = "***REMOVED***"
CHAT_ID = "-198071088"
REMINDER_DAYS = [30, 7, 1]

def load_concert_data():
    """Load concert data from JSON file. Works both locally and on AWS"""
    # Try AWS path first (flat structure)
    json_path = os.path.join('data', 'data.json')

    # If file not found, try local development path
    if not os.path.exists(json_path):
        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'data.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Could not find data.json at {json_path}")
        return {"concerts": []}

def check_reminders():
    """Check which concerts need reminders today"""
    data = load_concert_data()
    today = datetime.now().date()
    reminders = []
    
    for concert in data['concerts']:
        concert_date = datetime.strptime(concert['date'], '%Y-%m-%d').date()
        days_until = (concert_date - today).days
        
        if days_until in REMINDER_DAYS:
            reminders.append({
                'concert': concert,
                'days_until': days_until
            })
    
    return reminders

def format_reminder_message(reminder):
    """Format a reminder into a nice Telegram message"""
    concert = reminder['concert']
    days = reminder['days_until']
    
    # Basic concert info (same for all)
    message = f"`{concert['band']}`\n"
    message += f"`{concert['date']} u {concert['time']}`\n"
    message += f"`{concert['venue']}, {concert['city']}`\n"
    message += f"`Karta: {concert['ticket']}`\n\n"
    
    # Different messages based on days
    if days == 1:
        message += "🔥 Koncert je sutra, dobar provod ko ide, ko nejde stara baba\n\n"
        # No link for tomorrow reminders
    elif days == 7:
        message += "🎸 Koncert je za 7 dana, ako još niste kupili karte:\n\n"
        message += f"{concert['link']}\n\n"
    elif days == 30:
        message += "🎸 Koncert je za mjesec dana, jeste kupili karte?\n\n"
        message += f"{concert['link']}\n\n"
    else:
        message += f"🎸 Koncert je za {days} dana\n\n"
        message += f"{concert['link']}\n\n"
    
    message += "🤘🏿"
    
    return message

async def send_reminders():
    """Check for reminders and send them"""
    print(f"Checking reminders at {datetime.now()}")
    
    reminders = check_reminders()
    
    if not reminders:
        print("No reminders to send today.")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    for reminder in reminders:
        try:
            message = format_reminder_message(reminder)
            await bot.send_message(
                chat_id=CHAT_ID, 
                text=message, 
                parse_mode='Markdown'
            )
            
            concert = reminder['concert']
            days = reminder['days_until']
            print(f"✅ Sent {days}-day reminder for {concert['band']}")
            
        except Exception as e:
            print(f"❌ Failed to send reminder: {e}")

def main():
    """Main function"""
    try:
        asyncio.run(send_reminders())
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()