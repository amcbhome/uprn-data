import streamlit as st
import traceback
from fetch_and_store import update_database
from database import get_upcoming_collections, init_db

st.set_page_config(page_title="Bin Collection Dashboard", layout="centered")

# Ensure DB + table exist on startup
init_db()

st.title("♻️ Bin Collection Dashboard")

# --- Input ---
uprn = st.text_input("Enter UPRN", value="127072473")

# --- State ---
rows = []

# --- Action ---
if st.button("Access current information"):
    try:
        count = update_database(uprn)

        if count == 0:
            st.warning("Retrieved 0 events. Check if the UPRN is valid.")
        else:
            st.success(f"Retrieved and stored {count} events")

        rows = get_upcoming_collections(uprn)

    except Exception as e:
        st.error("An error occurred:")
        st.error(str(e))
        st.text(traceback.format_exc())

# --- Display ---
st.subheader("Upcoming Collections")

if rows:
    for date, type_ in rows:
        st.write(f"📅 {date} — {type_}")
else:
    st.info("No data available. Click the button above.")
