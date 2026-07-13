import re
from telegram import Update
from telegram.ext import ContextTypes
from services.exchange_api import convert_currency


async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Uso: /convertir <cantidad> <de> <a> <moneda>\n"
            "Ejemplo: /convertir 100 usd a cop\n"
            "         /convertir 50 euros a dolares"
        )
        return

    text = " ".join(context.args).lower()
    
    match = re.match(r'([\d.,]+)\s*(\w+)\s*a\s*(\w+)', text)
    if not match:
        await update.message.reply_text(
            "Formato no válido. Usa: /convertir 100 usd a cop"
        )
        return

    amount_str = match.group(1).replace(",", ".")
    from_currency = match.group(2)
    to_currency = match.group(3)

    try:
        amount = float(amount_str)
    except ValueError:
        await update.message.reply_text("La cantidad no es válida.")
        return

    CURRENCY_ALIASES = {
        "dolar": "USD", "dolares": "USD", "dollar": "USD", "dollars": "USD",
        "euro": "EUR", "euros": "EUR",
        "peso": "COP", "pesos": "COP",
        "pesos mexicanos": "MXN", "peso mexicano": "MXN",
        "libra": "GBP", "libras": "GBP", "pound": "GBP", "pounds": "GBP",
        "yen": "JPY", "yenes": "JPY",
        "real": "BRL", "reales": "BRL",
        "franco": "CHF", "francos": "CHF",
        "won": "KRW", "wones": "KRW",
        "yuan": "CNY", "yuanes": "CNY",
        "rublo": "RUB", "rublos": "RUB",
        "rupia": "INR", "rupias": "INR",
        "sol": "PEN", "soles": "PEN",
        "bolivar": "VES", "bolivares": "VES",
        "lempira": "HNL", "lempiras": "HNL",
        "quetzal": "GTQ", "quetzales": "GTQ",
        "colones": "CRC", "colon": "CRC",
        "balboa": "PAB", "balboas": "PAB",
        "cordoba": "NIO", "cordobas": "NIO",
        "guarani": "PYG", "guaranies": "PYG",
        "peso uruguayo": "UYU", "pesos uruguayos": "UYU",
        "dolar canadiense": "CAD", "dolares canadienses": "CAD",
        "dolar australiano": "AUD", "dolares australianos": "AUD",
        "dolar neozelandesa": "NZD",
        "corona sueca": "SEK", "coronas suecas": "SEK",
        "corona danesa": "DKK", "coronas danesas": "DKK",
        "corona noruega": "NOK", "coronas noruegas": "NOK",
        "zloty": "PLN", "zlotys": "PLN",
        "forinto": "HUF", "forintos": "HUF",
        "corona checa": "CZK", "coronas checas": "CZK",
        "rial": "SAR", "riales": "SAR",
        "dirham": "AED", "dirhams": "AED",
        "lira": "TRY", "liras": "TRY",
        "rand": "ZAR", "rands": "ZAR",
        "bitcoin": "BTC", "bitcoins": "BTC", "btc": "BTC",
        "ethereum": "ETH", "ethereumes": "ETH", "eth": "ETH",
    }

    from_currency = CURRENCY_ALIASES.get(from_currency, from_currency.upper())
    to_currency = CURRENCY_ALIASES.get(to_currency, to_currency.upper())

    await update.message.reply_text(f"Convirtiendo {amount} {from_currency} a {to_currency}...")

    result = convert_currency(amount, from_currency, to_currency)

    if "error" in result:
        await update.message.reply_text(f"Error: {result['error']}")
        return

    converted = result.get("result", 0)
    rate = result.get("rate", 0)
    date = result.get("date", "N/A")

    text = f"""
💱 Conversión de Moneda

{amount:,.2f} {from_currency} = {converted:,.2f} {to_currency}

Tasa: 1 {from_currency} = {rate:,.4f} {to_currency}
Fecha: {date}
"""
    await update.message.reply_text(text)
