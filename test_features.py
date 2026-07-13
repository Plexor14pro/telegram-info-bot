import sys
sys.stdout.reconfigure(encoding='utf-8')
from services.news_api import get_tech_news
from services.exchange_api import convert_currency

print("=== TECH NEWS ===")
result = get_tech_news(3)
for r in result:
    if "error" in r:
        print(f"ERROR: {r['error']}")
    else:
        print(f"OK: {r['title'][:60]}...")

print("\n=== CURRENCY CONVERSION ===")
result = convert_currency(100, "USD", "COP")
print(f"100 USD = {result.get('result', 'N/A')} COP")

result = convert_currency(50, "EUR", "USD")
print(f"50 EUR = {result.get('result', 'N/A')} USD")
