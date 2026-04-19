from database import init_db, insert_collections

def update_database(uprn):
    init_db()

    # --- Replace this with your real API call ---
    events = [
        {"date": "2026-04-20", "type": "General Waste"},
        {"date": "2026-04-27", "type": "Recycling"},
    ]
    # ------------------------------------------

    insert_collections(uprn, events)

    return len(events)
