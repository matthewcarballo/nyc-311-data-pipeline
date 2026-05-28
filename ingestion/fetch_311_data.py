import requests
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

if __name__ == "__main__":
    print("Fetching NYC 311 data...")
    data = fetch_311_data(limit=1000)
    save_to_csv(data)
    print("Done!")