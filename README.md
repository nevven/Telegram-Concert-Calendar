# Telegram-Concert-Calendar
Telegram bot that shows upcoming shows by date, place
Using [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) wrapper

## Unresolved Enhancement: Daily Album Release Notifications

### Attempted Feature
- Automatic notification at 9:00 AM when an album is releasing that day
- Should check album release dates in data.json
- Send formatted message to specified Telegram chat

### Implementation Attempts
1. Using APScheduler:
   - Added as direct dependency
   - Issues with async/await compatibility
   - Event loop conflicts

2. Using python-telegram-bot's JobQueue:
   - Attempted to use built-in scheduling
   - Required additional [job-queue] extension
   - Installation/dependency issues
   - JobQueue remained None despite proper installation

### Technical Challenges
- Event loop management in async environment
- Dependency conflicts
- Integration complexity exceeded the feature's simplicity

### Current Status
- Feature not implemented
- Using manual Telegram message scheduling as workaround
- May revisit with simpler approach (e.g., external cron job)

### Lessons Learned
- Simple features might not need complex scheduling libraries
- Consider external scheduling (cron) for basic time-based tasks
- Test scheduling implementations in isolation before integration