import requests
import re
from config import OPEN_METEO_URL

STOP_WORDS = {
    "de", "del", "la", "el", "en", "los", "las", "un", "una", "unos", "unas",
    "al", "a", "y", "o", "que", "por", "con", "para", "sin", "sobre", "entre",
    "desde", "hasta", "como", "mas", "menos", "muy", "poco", "mucho",
    "ciudad", "pueblo", "pais", "estado", "region", "provincia", "isla",
    "nuevo", "nueva", "viejo", "vieja",
    "grande", "pequeno", "pequena", "alto", "alta", "bajo", "baja",
    "norte", "sur", "este", "oeste", "oriente", "occidente",
    "donde", "cual", "como", "que", "cuando", "quien", "quien",
    "dame", "diga", "decime", "ponme", "muestrame", "informacion",
    "clima", "tiempo", "temperatura", "pronostico",
}

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

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def normalize_text(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_city_name(text: str) -> str:
    text = normalize_text(text)
    words = text.split()
    cleaned = [w for w in words if w not in STOP_WORDS]
    if not cleaned:
        cleaned = words
    return " ".join(cleaned).strip()


COUNTRY_PRIORITY = {
    "colombia": 100, "méxico": 100, "mexico": 100, "argentina": 100,
    "españa": 100, "spain": 100, "chile": 100, "perú": 100, "peru": 100,
    "venezuela": 100, "ecuador": 100, "bolivia": 100, "paraguay": 100,
    "uruguay": 100, "cuba": 100, "guatemala": 100, "honduras": 100,
    "el salvador": 100, "nicaragua": 100, "costa rica": 100, "panamá": 100,
    "república dominicana": 100, "puerto rico": 100,
    "japón": 90, "japan": 90, "reino unido": 90, "united kingdom": 90,
    "francia": 90, "france": 90, "alemania": 90, "germany": 90,
    "italia": 90, "italy": 90, "brasil": 90, "brazil": 90,
    "estados unidos": 80, "united states": 80, "usa": 80,
    "china": 80, "india": 80, "rusia": 80, "russia": 80,
}

MAJOR_CITIES = {
    "méxico": {"lat": 19.4326, "lon": -99.1332, "name": "Ciudad de México", "country": "México"},
    "mexico": {"lat": 19.4326, "lon": -99.1332, "name": "Ciudad de México", "country": "México"},
    "mexico city": {"lat": 19.4326, "lon": -99.1332, "name": "Ciudad de México", "country": "México"},
    "ciudad de mexico": {"lat": 19.4326, "lon": -99.1332, "name": "Ciudad de México", "country": "México"},
    "bogota": {"lat": 4.711, "lon": -74.0721, "name": "Bogotá", "country": "Colombia"},
    "bogotá": {"lat": 4.711, "lon": -74.0721, "name": "Bogotá", "country": "Colombia"},
    "tokyo": {"lat": 35.6762, "lon": 139.6503, "name": "Tokio", "country": "Japón"},
    "tokio": {"lat": 35.6762, "lon": 139.6503, "name": "Tokio", "country": "Japón"},
    "london": {"lat": 51.5074, "lon": -0.1278, "name": "Londres", "country": "Reino Unido"},
    "londres": {"lat": 51.5074, "lon": -0.1278, "name": "Londres", "country": "Reino Unido"},
    "paris": {"lat": 48.8566, "lon": 2.3522, "name": "París", "country": "Francia"},
    "parís": {"lat": 48.8566, "lon": 2.3522, "name": "París", "country": "Francia"},
    "new york": {"lat": 40.7128, "lon": -74.006, "name": "Nueva York", "country": "Estados Unidos"},
    "nueva york": {"lat": 40.7128, "lon": -74.006, "name": "Nueva York", "country": "Estados Unidos"},
    "los angeles": {"lat": 34.0522, "lon": -118.2437, "name": "Los Ángeles", "country": "Estados Unidos"},
    "angeles": {"lat": 34.0522, "lon": -118.2437, "name": "Los Ángeles", "country": "Estados Unidos"},
    "san jose": {"lat": 9.9281, "lon": -84.0907, "name": "San José", "country": "Costa Rica"},
    "san josé": {"lat": 9.9281, "lon": -84.0907, "name": "San José", "country": "Costa Rica"},
    "la paz": {"lat": -16.5, "lon": -68.15, "name": "La Paz", "country": "Bolivia"},
    "la paz bolivia": {"lat": -16.5, "lon": -68.15, "name": "La Paz", "country": "Bolivia"},
    "paz bolivia": {"lat": -16.5, "lon": -68.15, "name": "La Paz", "country": "Bolivia"},
    "paz": {"lat": -16.5, "lon": -68.15, "name": "La Paz", "country": "Bolivia"},
    "san jose costa rica": {"lat": 9.9281, "lon": -84.0907, "name": "San José", "country": "Costa Rica"},
    "san jose de costa rica": {"lat": 9.9281, "lon": -84.0907, "name": "San José", "country": "Costa Rica"},
    "san josé costa rica": {"lat": 9.9281, "lon": -84.0907, "name": "San José", "country": "Costa Rica"},
    "medellin": {"lat": 6.2476, "lon": -75.5658, "name": "Medellín", "country": "Colombia"},
    "medellín": {"lat": 6.2476, "lon": -75.5658, "name": "Medellín", "country": "Colombia"},
    "buenos aires": {"lat": -34.6037, "lon": -58.3816, "name": "Buenos Aires", "country": "Argentina"},
    "lima": {"lat": -12.0464, "lon": -77.0428, "name": "Lima", "country": "Perú"},
    "santiago": {"lat": -33.4489, "lon": -70.6693, "name": "Santiago", "country": "Chile"},
    "quito": {"lat": -0.1807, "lon": -78.4678, "name": "Quito", "country": "Ecuador"},
    "caracas": {"lat": 10.4806, "lon": -66.9036, "name": "Caracas", "country": "Venezuela"},
    "madrid": {"lat": 40.4168, "lon": -3.7038, "name": "Madrid", "country": "España"},
    "barcelona": {"lat": 41.3851, "lon": 2.1734, "name": "Barcelona", "country": "España"},
    "miami": {"lat": 25.7617, "lon": -80.1918, "name": "Miami", "country": "Estados Unidos"},
    "san juan": {"lat": 18.4655, "lon": -66.1057, "name": "San Juan", "country": "Puerto Rico"},
}


def score_result(result: dict, search_term: str, original: str) -> int:
    score = 0
    name = result.get("name", "").lower()
    country = result.get("country", "").lower()
    
    if name == search_term:
        score += 200
    elif search_term in name or name in search_term:
        score += 100
    
    for key, priority in COUNTRY_PRIORITY.items():
        if key in country:
            score += priority
            break
    
    return score


def geocode_city(city_name: str) -> dict:
    original = normalize_text(city_name)
    cleaned = clean_city_name(city_name)
    
    if cleaned in MAJOR_CITIES:
        data = MAJOR_CITIES[cleaned]
        return {
            "lat": data["lat"],
            "lon": data["lon"],
            "name": data["name"],
            "country": data["country"],
            "admin1": "",
        }
    
    attempts = []
    
    if original != cleaned:
        attempts.append(original)
    
    attempts.append(cleaned)
    
    for word in cleaned.split():
        if len(word) > 3 and word not in attempts:
            attempts.append(word)
    
    seen = set()
    unique_attempts = []
    for a in attempts:
        if a and a not in seen and len(a) > 1:
            seen.add(a)
            unique_attempts.append(a)
    
    for attempt_name in unique_attempts:
        for lang in ["es", "en"]:
            params = {
                "name": attempt_name,
                "count": 10,
                "format": "json",
                "language": lang,
            }
            try:
                response = requests.get(GEOCODING_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])
                if results:
                    best = None
                    best_score = -1
                    for r in results:
                        s = score_result(r, attempt_name, original)
                        if s > best_score:
                            best_score = s
                            best = r
                    
                    if best:
                        return {
                            "lat": best.get("latitude"),
                            "lon": best.get("longitude"),
                            "name": best.get("name", city_name),
                            "country": best.get("country", ""),
                            "admin1": best.get("admin1", ""),
                        }
            except Exception:
                continue
    
    return None


def get_weather(city: str) -> dict:
    cleaned = clean_city_name(city)
    geo = geocode_city(city)
    if not geo:
        return {"error": f"No encontré \"{cleaned}\". Intenta solo con el nombre de la ciudad (ej: Madrid, Tokyo, Buenos Aires)."}

    coords = {"lat": geo["lat"], "lon": geo["lon"]}
    city_display = geo["name"]
    if geo.get("admin1"):
        city_display += f", {geo['admin1']}"
    if geo.get("country"):
        city_display += f", {geo['country']}"

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
            "city": city_display,
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
