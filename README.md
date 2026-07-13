# 🤖 Bot de Telegram - Información

Bot de Telegram para consultar información en tiempo real: clima, tipo de cambio, criptomonedas y noticias.

## Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `/start` | Bienvenida |
| `/ayuda` | Lista de comandos |
| `/clima <ciudad>` | Clima actual |
| `/dolar` | Tipo de cambio USD |
| `/euro` | Tipo de cambio EUR |
| `/crypto` | Top 10 criptomonedas |
| `/crypto bitcoin` | Precio de una crypto específica |
| `/noticias` | Últimas noticias |
| `/tech` | Noticias de tecnología |

## Requisitos

- Python 3.8+
- Token de Bot de Telegram (obtener de @BotFather)

## Instalación

1. Clonar o descargar el proyecto:
```bash
cd telegram-bot
```

2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
copy .env.example .env
```

5. Editar `.env` con tu token:
```
TELEGRAM_TOKEN=tu_token_aqui
NEWS_API_KEY=tu_api_key_aqui  # Opcional
```

6. Ejecutar el bot:
```bash
python bot.py
```

## APIs Utilizadas

- **Clima**: Open-Meteo (gratuita, sin API key)
- **Tipo de cambio**: Frankfurter (gratuita, sin API key)
- **Criptomonedas**: CoinGecko (gratuita, sin API key)
- **Noticias tech**: WhatsTrending (gratuita, sin API key)
- **Noticias generales**: NewsAPI (requiere API key gratuita)

## Estructura

```
telegram-bot/
├── bot.py              # Archivo principal
├── config.py           # Configuración
├── handlers/           # Comandos del bot
│   ├── start.py
│   ├── weather.py
│   ├── exchange.py
│   ├── crypto.py
│   └── news.py
├── services/           # Lógica de APIs
│   ├── weather_api.py
│   ├── exchange_api.py
│   ├── crypto_api.py
│   └── news_api.py
├── requirements.txt
└── .env.example
```

## Notas

- Las APIs de clima, tipo de cambio y crypto no requieren API key
- NewsAPI es gratuita pero requiere registro en newsapi.org
- El bot está configurado por defecto para ciudades de Latinoamérica
