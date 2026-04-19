import os
import requests
import sqlite3
from datetime import datetime

DB_PATH = "data/waste.db"

def fetch_ics(uprn: str):
    """Fetch ICS calendar from East Ayrshire council"""
    url = "https://www.east-ayrshire.gov.uk/WasteCalendarICSDownload"
    
    data = {
        "uprn": uprn,
        "captchaResponse": ""
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise Exception("API request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch calendar data: {str(e)}")
    
    if "BEGIN:VCALENDAR" not in response.text:
        raise Exception("Invalid UPRN or no calendar data available")
    
    return response.text


def parse_ics(ics_text: str):
    """Parse ICS format calendar text"""
    events = []
    lines = ics_text.splitlines()
    current_event = {}
    
    for line in lines:
        line = line.strip()
        
        if line == "BEGIN:VEVENT":
            current_event = {}
        
        elif line.startswith("DTSTART"):
            try:
                date = line.split(":", 1)[1]  # Fixed: use split(":", 1) to handle colons in values
                date = datetime.strptime(date, "%Y%m%d").date()
                current_event["date"] = str(date)
            except (ValueError, IndexError):
                continue
        
        elif line.startswith("SUMMARY"):
            try:
                current_event["type"] = line.split(":", 1)[1]  # Fixed: use split(":", 1)
            except IndexError:
                continue
        
        elif line == "END:VEVENT":
            if "date" in current_event and "type" in current_event:
                events.append((current_event["date"], current_event["type"]))
    
    return events


def store_events(events):
    """Store events in SQLite database"""
    # Ensure data directory exists - FIXED
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with sqlite3.connect(DB_PATH) as conn:  # FIXED: use context manager
        cur = conn.cursor()
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS collections (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            UNIQUE(date, type)
        )
        """)
        
        cur.execute("DELETE FROM collections")
        cur.executemany("INSERT INTO collections VALUES (NULL, ?, ?)", events)
        
        conn.commit()


def update_database(uprn: str):
    """Main function to fetch, parse, and store waste collection data"""
    ics = fetch_ics(uprn)
    events = parse_ics(ics)
    store_events(events)
    return len(events)
