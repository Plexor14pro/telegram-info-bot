import requests
from config import OPEN_METEO_URL, WEATHER_COMMANDS

WMO_CODES = {
    0: "☀️ Despejado",
    1: "🌤️ Principalmente despejado",
    2: "⛅ Parcialmente nublado",
    3: "☁️ Nublado",
    45: "🌫️ Niebla",
    48: "🌫️ Niebla con escarcha",
    51: "🌦️ Lluvia ligera",
    53: "🌦️ Lluvia moderada",
    55: "🌧️ Lluvia intensa",
    61: "🌧️ Lluvia",
    63: "🌧️ Lluvia moderada",
    65: "🌧️ Lluvia fuerte",
    71: "❄️ Nieve ligera",
    73: "❄️ Nieve moderada",
    75: "❄️ Nieve fuerte",
    80: "🌦️ Chaparrones ligeros",
    81: "🌧️ Chaparrones moderados",
    82: "⛈️ Chaparrones fuertes",
    95: "⛈️ Tormenta",
    96: "⛈️ Tormenta con granizo",
    99: "⛈️ Tormenta con granizo fuerte",
}


def get_weather(city: str) -> dict:
    city_lower = city.lower().replace(" ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

    if city_lower in WEATHER_COMMANDS:
        coords = WEATHER_COMMANDS[city_lower]
    else:
        coords = {"lat": 4.711, "lon": -74.0721}
        city = "Bogotá"

    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 1,
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data.get("current", {})
        daily = data.get("daily", {})

        temp = current.get("temperature_2m", "N/A")
        feels_like = current.get("apparent_temperature", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        weather_code = current.get("weather_code", 0)
        wind = current.get("wind_speed_10m", "N/A")

        temp_max = daily.get("temperature_2m_max", ["N/A"])[0]
        temp_min = daily.get("temperature_2m_min", ["N/A"])[0]
        precip_prob = daily.get("precipitation_probability_max", ["N/A"])[0]

        weather_desc = WMO_CODES.get(weather_code, "❓ Desconocido")

        return {
            "city": city.title(),
            "weather": weather_desc,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind": wind,
            "temp_max": temp_max,
            "temp_min": temp_min,
            "precip_prob": precip_prob,
        }
    except Exception as e:
        return {"error": str(e)}
