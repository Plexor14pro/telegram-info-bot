import requests
from config import NEWSAPI_URL, NEWS_API_KEY, WHATSTRENDING_URL


def get_general_news(limit: int = 5) -> list:
    if not NEWS_API_KEY:
        return [{"error": "NEWS_API_KEY no configurada"}]

    try:
        url = f"{NEWSAPI_URL}/top-headlines"
        params = {
            "country": "co",
            "pageSize": limit,
            "apiKey": NEWS_API_KEY,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])
        return [
            {
                "title": a.get("title", "Sin título"),
                "description": a.get("description", "Sin descripción"),
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", "Desconocido"),
            }
            for a in articles
        ]
    except Exception as e:
        return [{"error": str(e)}]


def get_tech_news(limit: int = 5) -> list:
    try:
        url = f"{WHATSTRENDING_URL}/articles"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])[:limit]
        return [
            {
                "title": a.get("title", "Sin título"),
                "summary": a.get("summary", "Sin resumen"),
                "source": a.get("source", "Desconocido"),
                "category": a.get("category", "General"),
            }
            for a in articles
        ]
    except Exception as e:
        return [{"error": str(e)}]
