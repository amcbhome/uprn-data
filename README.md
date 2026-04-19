# ♻️ Bin Collection Dashboard (UPRN-Powered)

## 📌 Overview

This project is a **Streamlit-based dashboard** that retrieves and displays household waste collection schedules using a **Unique Property Reference Number (UPRN)**.

The application demonstrates a full data pipeline:

> **UPRN → API request → ICS data → parsing → SQLite storage → dashboard display**

It is designed as a **portable, lightweight data product** that can run locally or in the cloud, and forms part of a broader **UPRN-based local services dashboard** concept.

---

## 🧭 What is a UPRN?

A **UPRN (Unique Property Reference Number)** is a unique identifier assigned to every addressable location in the UK.

* Issued and maintained by: **Ordnance Survey (OS)**
* Used across:

  * Local councils
  * NHS
  * Emergency services
  * Utilities and infrastructure systems

### 🔍 Why UPRN matters

Unlike postcodes (which represent areas), a UPRN identifies a **specific property**.

This enables:

* Precise service delivery (e.g. bin collections)
* Data integration across systems
* Property-level analytics and dashboards

👉 In this project, the UPRN is used to retrieve **property-specific waste collection schedules**.

---

## 🌐 How the Data is Retrieved

The application sends a **POST request** to the East Ayrshire Council endpoint:

```
https://www.east-ayrshire.gov.uk/WasteCalendarICSDownload
```

### Request payload:

```python
data = {
    "uprn": "127072473",
    "captchaResponse": ""
}
```

### 📥 Response format: ICS (iCalendar)

The server returns data in **ICS format**, which is commonly used for calendar events (e.g. Outlook, Google Calendar).

Example structure:

```
BEGIN:VEVENT
DTSTART:20260407
SUMMARY:trolley and food bin
END:VEVENT
```

---

## 🔄 Data Processing Pipeline

### Step 1 — Fetch

* ICS file retrieved via HTTP POST request

### Step 2 — Parse

* Extract:

  * `DTSTART` → collection date
  * `SUMMARY` → bin type

### Step 3 — Transform

* Convert dates into readable format (`YYYY-MM-DD`)

### Step 4 — Store

* Insert into SQLite database

### Step 5 — Display

* Query upcoming collections in Streamlit

---

## 🗄️ What is SQLite?

**SQLite** is a lightweight, serverless relational database stored as a single file:

```
waste.db
```

### Key Characteristics

* No server required
* Zero configuration
* Fully portable (just copy the file)
* ACID-compliant (reliable transactions)

---

## 🚀 Why SQLite is Important for This Project

SQLite enables this application to function as a **portable data product**:

### ✔ Local-first architecture

* Works offline after data retrieval
* No dependency on external database servers

### ✔ Simple deployment

* Ideal for:

  * Streamlit Cloud
  * Home dashboards
  * Embedded systems (e.g. Fire TV / Raspberry Pi)

### ✔ Reusable dataset

* The `.db` file can be:

  * Queried with SQL
  * Connected to BI tools (e.g. Apache Superset)
  * Exported to CSV for analysis

---

## 📊 Example Database Schema

```sql
CREATE TABLE collections (
    date TEXT,
    type TEXT
);
```

---

## 🖥️ Streamlit Dashboard Features

* Input UPRN
* Button: **"Access current information"**
* Live data retrieval and refresh
* Display of upcoming bin collections

---

## 🧠 Project Significance

This project demonstrates:

### 🔹 Data Engineering

* API interaction (POST request)
* Parsing semi-structured data (ICS)

### 🔹 Data Storage

* SQLite database design and usage

### 🔹 Analytics Thinking

* Property-level data modelling using UPRN

### 🔹 Dashboard Development

* Interactive UI using Streamlit

---

## 🌍 Future Development (Roadmap)

This is intended as a **module within a larger UPRN dashboard**, including:

* 🚌 Live bus departures (Transport APIs)
* 🗺️ Geospatial mapping (UPRN → coordinates)
* 🏪 Local services (shops, opening times)
* 🚶 Walking distances and travel times

---

## ⚙️ Installation & Running

```bash
git clone https://github.com/your-username/waste-dashboard.git
cd waste-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
waste-dashboard/
│
├── app.py
├── fetch_and_store.py
├── database.py
├── requirements.txt
├── README.md
└── data/
    └── waste.db
```

---

## 📌 Key Insight

> This project illustrates how a **single identifier (UPRN)** can unlock multiple datasets and enable **property-level intelligence systems**.

It reflects real-world approaches used in:

* Smart cities
* Government data integration
* Operational dashboards

---

## 📜 Disclaimer

This project is for **educational and demonstration purposes**.
Data is retrieved from a publicly accessible council endpoint and should be used responsibly.

---

## 👤 Author

Alastair McBride
