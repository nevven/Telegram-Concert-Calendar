#!/usr/bin/env python3
from datetime import datetime, timedelta
import json
import os

def load_concert_data():
    """Load concert data from JSON file"""
    # Try the same path logic as your bot
    json_path = os.path.join('..', 'data', 'data.json')
    
    # If file not found, try current directory
    if not os.path.exists(json_path):
        json_path = 'data.json'
    
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
    
    print(f"Today is: {today}")
    print(f"Checking {len(data['concerts'])} concerts...")
    print()
    
    for concert in data['concerts']:
        concert_date = datetime.strptime(concert['date'], '%Y-%m-%d').date()
        days_until = (concert_date - today).days
        
        print(f"{concert['band']} ({concert['date']}) - {days_until} days away")
        
        if days_until in [30, 7, 1]:
            reminders.append({
                'concert': concert,
                'days_until': days_until
            })
            print(f"  ⚠️  REMINDER NEEDED: {days_until} days!")
        
        # Also show if concert has passed
        if days_until < 0:
            print(f"  ❌ Concert has passed")
    
    return reminders

def main():
    print("=== Concert Reminder Test ===")
    print()
    
    reminders = check_reminders()
    
    print()
    print("=== SUMMARY ===")
    if reminders:
        print(f"Found {len(reminders)} reminders to send:")
        for reminder in reminders:
            concert = reminder['concert']
            days = reminder['days_until']
            print(f"  • {days} days until {concert['band']} in {concert['city']}")
    else:
        print("No reminders needed today.")

if __name__ == "__main__":
    main()