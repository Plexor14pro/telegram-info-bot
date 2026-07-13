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
