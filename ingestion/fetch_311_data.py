import requests
import psycopg2
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
def fetch_311_data(limit=1000, offset=0):
    """Fetch NYC 311 service requests from the Open Data API."""
    url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
    params = {
        "$limit": limit,
        "$offset": offset,
        "$order": "created_date DESC"
    }
    print(f"Calling API: {url}")
    response = requests.get(url, params=params, timeout=30)
    print(f"Status code: {response.status_code}")
    response.raise_for_status()
    data = response.json()
    print(f"Records returned: {len(data)}")
    return data

def save_to_csv(data, filename=None):
    """Save fetched data to a CSV file."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/raw_311_{timestamp}.csv"
    
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} records to {filename}")
    return filename

def load_to_postgres(filename):
    """Load CSV data into PostgreSQL database."""
    df = pd.read_csv(filename)

    conn = psycopg2.connect(
        dbname="nyc_311",
        user=os.environ.get("USER"),
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_311 (
            unique_key TEXT,
            created_date TEXT,
            closed_date TEXT,
            agency TEXT,
            agency_name TEXT,
            complaint_type TEXT,
            descriptor TEXT,
            incident_zip TEXT,
            city TEXT,
            status TEXT,
            borough TEXT,
            latitude TEXT,
            longitude TEXT
        )
    """)

    count = 0
    for _, row in df[['unique_key','created_date','closed_date','agency',
                       'agency_name','complaint_type','descriptor',
                       'incident_zip','city','status','borough',
                       'latitude','longitude']].iterrows():
        cursor.execute("""
            INSERT INTO raw_311 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT DO NOTHING
        """, tuple(row))
        count += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Loaded {count} records into PostgreSQL!")

if __name__ == "__main__":
    print("Fetching NYC 311 data...")
    data = fetch_311_data(limit=1000)
    filename = save_to_csv(data)
    try:
        load_to_postgres(filename)
    except Exception as e:
        print(f"Error loading to PostgreSQL: {e}")
    print("Done!")
