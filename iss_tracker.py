import requests
from datetime import datetime

def get_iss_position():
    url = "http://api.open-notify.org/iss-now.json"

    response = requests.get(url, timeout=5)
    response.raise_for_status()

    data = response.json()
    lat = float(data["iss_position"]["latitude"])
    lon = float(data["iss_position"]["longitude"])
    timestamp = datetime.fromtimestamp(data["timestamp"])

    print("=" * 40)
    print("  ISS Current Position")
    print("=" * 40)
    print(f"  Latitude  : {lat:.4f}°")
    print(f"  Longitude : {lon:.4f}°")
    print(f"  Time (UTC): {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)

if __name__ == "__main__":
    get_iss_position()
