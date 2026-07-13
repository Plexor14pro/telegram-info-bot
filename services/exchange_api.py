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
