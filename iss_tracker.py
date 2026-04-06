import requests
import csv
import os
from datetime import datetime

CSV_FILE = "iss_log.csv"

def get_iss_position():
    url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        lat = float(data["iss_position"]["latitude"])
        lon = float(data["iss_position"]["longitude"])
        timestamp = datetime.fromtimestamp(data["timestamp"])
        return lat, lon, timestamp
    except requests.exceptions.ConnectionError:
        print("  ERROR: No internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("  ERROR: Request timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"  ERROR: API returned an error: {e}")
        return None

def get_astronaut_count():
    url = "http://api.open-notify.org/astros.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["number"], [p["name"] for p in data["people"]]
    except requests.exceptions.ConnectionError:
        print("  ERROR: No internet connection.")
        return None, []
    except requests.exceptions.Timeout:
        print("  ERROR: Request timed out.")
        return None, []
    except requests.exceptions.HTTPError as e:
        print(f"  ERROR: API returned an error: {e}")
        return None, []

def save_to_csv(lat, lon, timestamp, astronaut_count):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "latitude", "longitude", "people_in_space"])
        writer.writerow([timestamp.strftime("%Y-%m-%d %H:%M:%S"), lat, lon, astronaut_count])
    print(f"  Logged to {CSV_FILE}")

if __name__ == "__main__":
    print("=" * 40)
    print("  ISS Current Position")
    print("=" * 40)

    result = get_iss_position()
    if result:
        lat, lon, timestamp = result
        print(f"  Latitude  : {lat:.4f}°")
        print(f"  Longitude : {lon:.4f}°")
        print(f"  Time (UTC): {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("  Could not retrieve ISS position.")

    print("=" * 40)

    count, names = get_astronaut_count()
    if count is not None:
        print(f"  People in space : {count}")
        for name in names:
            print(f"    - {name}")
    else:
        print("  Could not retrieve astronaut data.")

    print("=" * 40)

    if result and count is not None:
        save_to_csv(lat, lon, timestamp, count)