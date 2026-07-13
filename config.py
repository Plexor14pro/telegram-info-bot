import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
FRANKFURTER_URL = "https://api.frankfurter.dev"
COINGECKO_URL = "https://api.coingecko.com/api/v3"
WHATSTRENDING_URL = "https://whatstrending.ai/api"
NEWSAPI_URL = "https://newsapi.org/v2"

DEFAULT_CITY = "Bogotá"

WEATHER_COMMANDS = {
    "bogota": {"lat": 4.711, "lon": -74.0721},
    "medellin": {"lat": 6.2476, "lon": -75.5658},
    "cali": {"lat": 3.4372, "lon": -76.5225},
    "barranquilla": {"lat": 10.9685, "lon": -74.7813},
    "cartagena": {"lat": 10.391, "lon": -75.5144},
    "buenosaires": {"lat": -34.6037, "lon": -58.3816},
    "mexico": {"lat": 19.4326, "lon": -99.1332},
    "madrid": {"lat": 40.4168, "lon": -3.7038},
    "barcelona": {"lat": 41.3851, "lon": 2.1734},
    "newyork": {"lat": 40.7128, "lon": -74.006},
    "miami": {"lat": 25.7617, "lon": -80.1918},
    "lima": {"lat": -12.0464, "lon": -77.0428},
    "santiago": {"lat": -33.4489, "lon": -70.6693},
    "quito": {"lat": -0.1807, "lon": -78.4678},
    "caracas": {"lat": 10.4806, "lon": -66.9036},
}
