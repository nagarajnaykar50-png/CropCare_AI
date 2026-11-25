import requests
from flask import current_app


def get_weather(latitude, longitude):

    api_key = current_app.config.get("WEATHER_API_KEY")

    if not api_key:

        return {
            "success": False,
            "mode": "unconfigured",
            "message": "Weather API key is not configured.",
            "latitude": latitude,
            "longitude": longitude
        }

    try:

        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": latitude,
                "lon": longitude,
                "appid": api_key,
                "units": "metric"
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {
            "success": True,
            "mode": "live",
            "location": data.get("name"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }

    except requests.RequestException:

        return {
            "success": False,
            "message": "Unable to retrieve live weather data."
        }

    except (KeyError, TypeError, ValueError):

        return {
            "success": False,
            "message": "Weather provider returned invalid data."
        }