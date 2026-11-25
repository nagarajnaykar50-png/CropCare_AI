import requests, json, numpy as np

def weather_risk(lat, lon):
    try:
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
               "&hourly=temperature_2m,relative_humidity_2m,precipitation&forecast_days=3")
        h = requests.get(url, timeout=10).json()["hourly"]
        temp = float(np.mean(h["temperature_2m"]))
        hum = float(np.mean(h["relative_humidity_2m"]))
        rain = float(sum(h["precipitation"]))
        json.dump({"temp": temp, "hum": hum, "rain": rain},
                  open("cache/weather_backup.json", "w"))
    except Exception:
        d = json.load(open("cache/weather_backup.json"))   # internet fail
        temp, hum, rain = d["temp"], d["hum"], d["rain"]

    score = 0
    if 10 <= temp <= 25: score += 0.4
    if hum >= 85:        score += 0.4
    if rain > 2:         score += 0.2
    return score