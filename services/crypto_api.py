import requests
from config import COINGECKO_URL


def get_top_coins(limit: int = 10) -> list:
    try:
        url = f"{COINGECKO_URL}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return [{"error": str(e)}]


def get_coin_price(coin_id: str) -> dict:
    try:
        url = f"{COINGECKO_URL}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": True,
            "include_market_cap": True,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if coin_id in data:
            coin_data = data[coin_id]
            return {
                "id": coin_id,
                "price_usd": coin_data.get("usd", "N/A"),
                "change_24h": coin_data.get("usd_24h_change", "N/A"),
                "market_cap": coin_data.get("usd_market_cap", "N/A"),
            }
        return {"error": "Moneda no encontrada"}
    except Exception as e:
        return {"error": str(e)}
