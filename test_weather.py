import sys
sys.stdout.reconfigure(encoding='utf-8')
from services.weather_api import get_weather, clean_city_name

tests = [
    "en la ciudad de guatemala",
    "de la ciudad de buenos aires",
    "la ciudad de mexico",
    "ciudad de medellin",
    "en san jose de costa rica",
    "el salvador",
    "la paz bolivia",
    "santiago de chile",
    "bogota",
    "tokyo",
    "london",
    "paris",
    "new york",
    "los angeles",
    "san juan",
]

for t in tests:
    print(f"\nInput: '{t}'")
    cleaned = clean_city_name(t)
    print(f"  Cleaned: '{cleaned}'")
    result = get_weather(t)
    if "error" in result:
        print(f"  ERROR: {result['error']}")
    else:
        print(f"  OK: {result['city']} - {result['temp']}°C")
