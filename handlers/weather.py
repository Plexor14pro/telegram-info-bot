from telegram import Update
from telegram.ext import ContextTypes
from services.weather_api import get_weather
from config import DEFAULT_CITY


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args) if context.args else DEFAULT_CITY

    await update.message.reply_text(f"Obteniendo clima de {city}...")

    result = get_weather(city)

    if "error" in result:
        await update.message.reply_text(f"Error al obtener el clima: {result['error']}")
        return

    text = f"""
{result['weather']}

Ciudad: {result['city']}
Temperatura: {result['temp']}°C
Sensación térmica: {result['feels_like']}°C
Humedad: {result['humidity']}%
Viento: {result['wind']} km/h

Máxima: {result['temp_max']}°C
Mínima: {result['temp_min']}°C
Prob. lluvia: {result['precip_prob']}%
"""
    await update.message.reply_text(text)
