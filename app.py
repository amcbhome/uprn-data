import streamlit as st
import requests
import traceback
from datetime import datetime

st.set_page_config(page_title="Bin Collection Dashboard", layout="centered")

st.title("♻️ Bin Collection Dashboard")

# --- CONFIG ---
API_URL = "https://api.example.com/collections?uprn={uprn}"


# --- FETCH FUNCTION ---
@st.cache_data(ttl=3600)
def fetch_collections(uprn):
    url = API_URL.format(uprn=uprn)

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")

    data = response.json()

    return normalise_events(data)


# --- TRANSFORM FUNCTION ---
def normalise_events(api_data):
    events = []

    # ⚠️ Adjust this depending on your real API structure
    for item in api_data.get("collections", []):
        try:
            raw_date = item.get("date")
            waste_type = item.get("type", "Unknown")

            date_obj = datetime.fromisoformat(raw_date)
            clean_date = date_obj.strftime("%Y-%m-%d")

            events.append((clean_date, waste_type))

        except Exception:
            continue

    return events


# --- INPUT ---
uprn = st.text_input("Enter UPRN", value="127072473")

# --- SESSION STATE ---
if "rows" not in st.session_state:
    st.session_state.rows = []

# --- ACTION ---
if st.button("Access current information"):
    try:
        rows = fetch_collections(uprn)

        if not rows:
            st.warning("No collection data found for this UPRN.")
        else:
            st.success(f"Retrieved {len(rows)} events")

        st.session_state.rows = rows

    except Exception as e:
        st.error("An error occurred:")
        st.error(str(e))
        st.text(traceback.format_exc())


# --- DISPLAY ---
st.subheader("Upcoming Collections")

if st.session_state.rows:
    for date, type_ in st.session_state.rows[:5]:
        st.write(f"📅 {date} — {type_}")
else:
    st.info("No data available. Enter a UPRN and click the button.")
