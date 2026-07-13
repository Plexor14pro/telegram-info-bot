import requests
from config import FRANKFURTER_URL


def get_exchange_rate(base: str = "USD", target: str = "COP") -> dict:
    try:
        url = f"{FRANKFURTER_URL}/latest?from={base}&to={target}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        rate = data.get("rates", {}).get(target, "N/A")
        date = data.get("date", "N/A")

        return {
            "base": base,
            "target": target,
            "rate": rate,
            "date": date,
        }
    except Exception as e:
        return {"error": str(e)}


def get_multiple_rates(base: str = "USD", targets: list = None) -> dict:
    if targets is None:
        targets = ["COP", "EUR", "MXN", "ARS", "PEN"]

    try:
        symbols = ",".join(targets)
        url = f"{FRANKFURTER_URL}/latest?from={base}&to={symbols}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})
        date = data.get("date", "N/A")

        return {
            "base": base,
            "rates": rates,
            "date": date,
        }
    except Exception as e:
        return {"error": str(e)}


CONVERT_API_URL = "https://open.er-api.com/v6/latest"


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    try:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        url = f"{CONVERT_API_URL}/{from_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})
        rate = rates.get(to_currency)
        
        if rate is None:
            return {"error": f"No encontré la moneda: {to_currency}"}
        
        converted = amount * rate
        date = data.get("time_last_update_utc", "N/A")

        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "result": converted,
            "rate": rate,
            "date": date,
        }
    except Exception as e:
        return {"error": str(e)}
