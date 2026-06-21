"""
HiveBox API - A DevOps tooling API
version 0.1.0
"""

import random
from datetime import datetime, timezone, timedelta
from flask import Flask
import requests

app = Flask(__name__)

# OpenSenseMap API base URL
OPENSENSEMAP_API = "https://api.opensensemap.org"

def get_temperature_boxes():
    """Fetch senseBoxes that have temperature sensors with recent data."""
    url = f"{OPENSENSEMAP_API}/boxes"

    # Use date parameter to get only boxes with recent measurements (last hour)
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    date_str = one_hour_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    params = {"phenomenon": "temperature", "date": date_str, "format": "json"}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def get_latest_temperature(box):
    """Extract the latest temperature reading from a senseBox."""
    for sensor in box.get("sensors", []):
        title = sensor.get("title", "").lower()
        # Look for temperature sensors (various naming conventions)
        if "temp" in title and "humidity" not in title:
            measurement = sensor.get("lastMeasurement")
            if measurement and isinstance(measurement, dict):
                value = measurement.get("value")
                if value:
                    try:
                        return float(value)
                    except (ValueError, TypeError):
                        continue
    return None


def get_average_temperature_from_boxes(num_boxes=3):
    """Get average temperature from random OpenSenseMap boxes."""
    # Fetch boxes with temperature sensors
    boxes = get_temperature_boxes()

    if not boxes:
        return None, "No temperature boxes found"

    # Filter boxes that have valid recent temperature readings
    valid_boxes = []
    for box in boxes:
        temp = get_latest_temperature(box)
        if temp is not None:
            valid_boxes.append({"box": box, "temperature": temp})

    if len(valid_boxes) < num_boxes:
        return None, f"Only {len(valid_boxes)} boxes with valid readings found"

    # Select random boxes
    selected = random.sample(valid_boxes, num_boxes)
    temperatures = [item["temperature"] for item in selected]

    # Calculate average
    avg_temp = sum(temperatures) / len(temperatures)

    return avg_temp, None


@app.route("/")
def main():
    """Main route for the hivebox API that returns a welcome message."""
    return "<p>Welcome to your HiveBox</p>"


@app.route("/version")
def version():
    """Version route for the hivebox API."""
    return "<p>Version: 0.1.0</p>"


@app.route("/temp")
def temperature():
    """Return average temperature from 3 random OpenSenseMap boxes."""
    avg_temp, error = get_average_temperature_from_boxes(num_boxes=3)

    if error:
        return f"<p>Error: {error}</p>", 500

    return f"<p>Average Temperature: {avg_temp:.2f}°C</p>"


if __name__ == "__main__":
    app.run(debug=True)
