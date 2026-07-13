from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
¡Hola! 👋 Soy tu bot de información.

Comandos disponibles:

/clima <ciudad> - Clima actual
/dolar - Tipo de cambio USD
/euro - Tipo de cambio EUR
/crypto - Top 10 criptomonedas
/crypto <moneda> - Precio de una crypto
/noticias - Últimas noticias
/tech - Noticias de tecnología
/ayuda - Lista de comandos

Ejemplo: /clima medellin
"""
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Lista de comandos:

/clima <ciudad> - Clima de una ciudad
/dolar - Precio del dólar
/euro - Precio del euro
/crypto - Top 10 criptomonedas
/crypto bitcoin - Precio de Bitcoin
/noticias - Noticias generales
/tech - Noticias de tecnología

Ciudades disponibles: bogota, medellin, cali, barranquilla, cartagena, buenosaires, mexico, madrid, barcelona, newyork, miami, lima, santiago, quito, caracas
"""
    await update.message.reply_text(help_text)
