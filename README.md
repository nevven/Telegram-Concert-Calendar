# Telegram Concert Calendar Bot

Uses [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) wrapper.


## Features

- **Concert listings** - `/koncerti` command shows all upcoming concerts
- **Album releases** - `/albumi` command shows upcoming album releases  
- **Automatic reminders** - Daily notifications for concerts at 30, 7, and 1 day intervals

## Bot Commands

- `/help` - Show help message
- `/koncerti` - Show upcoming concerts (Raspored Koncerata)
- `/albumi` - Show upcoming album releases (Nadolazeći Albumi)
- `/chatid` - Get current chat ID (for setup) # not coded in

## Configuration

### Telegram Settings
- **Bot Token**: `***REMOVED***`
- **Main Group Chat ID**: `-198071088`
- **Test Group Chat ID**: `-4604558871`

### Reminder Schedule
- **30 days before** - "jeste kupili karte?" reminder
- **7 days before** - "ako još niste kupili karte" reminder  
- **1 day before** - "sutra je koncert" reminder

## Files

- `bot.py` - Main bot server with command handlers
- `send_reminders.py` - Daily reminder checker and sender
- `data/data.json` - Concert and album data

## Deployment

### AWS EC2 Setup
Bot runs as a systemd service on AWS EC2 free tier:

```bash
# Control the bot service
sudo systemctl start telegram-bot
sudo systemctl stop telegram-bot  
sudo systemctl restart telegram-bot
sudo systemctl status telegram-bot
```

### Daily Reminders
Set up cron job to run reminder checker daily:

```bash
# Edit crontab
crontab -e

# Add daily reminder at 9:00 AM
0 9 * * * /usr/bin/python3 /home/ec2-user/telegram-concert-calendar/send_reminders.py
```

## Data Format

Concert data is stored in `data/data.json`:

```json
{
    "concerts": [
        {
            "band": "Band Name",
            "date": "YYYY-MM-DD",
            "time": "HH:MM",
            "city": "City",
            "venue": "Venue Name",
            "ticket": "€XX",
            "link": "https://ticket-link"
        }
    ],
    "albums": [
        {
            "band": "Band Name",
            "album": "Album Title",
            "date": "YYYY-MM-DD",
            "label": "Record Label"
        }
    ]
}
```

## Development Notes

### File Structure
- **AWS**: Flat structure (bot.py and data/ in same directory)
- **Local**: src/ folder structure with data/ at project root

### Solved: Daily Reminder Notifications
Successfully implemented automatic concert reminders using:
- Simple daily script (`send_reminders.py`) 
- System cron job for scheduling
- Direct Telegram Bot API for message sending

**Previous attempts with APScheduler and JobQueue were overly complex** - the simple approach works reliably and is easier to maintain.

### Testing
Use test group chat ID `-4604558871` for testing reminders without spamming main group.