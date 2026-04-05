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
    return lat, lon, timestamp

def get_astronaut_count():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    return data["number"], [p["name"] for p in data["people"]]

if __name__ == "__main__":
    lat, lon, timestamp = get_iss_position()
    count, names = get_astronaut_count()

    print("=" * 40)
    print("  ISS Current Position")
    print("=" * 40)
    print(f"  Latitude  : {lat:.4f}°")
    print(f"  Longitude : {lon:.4f}°")
    print(f"  Time (UTC): {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)
    print(f"  People in space : {count}")
    for name in names:
        print(f"    - {name}")
    print("=" * 40)