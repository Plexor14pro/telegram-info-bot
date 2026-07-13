from telegram import Update
from telegram.ext import ContextTypes
from services.exchange_api import get_exchange_rate, get_multiple_rates


async def dollar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Obteniendo tipo de cambio...")

    result = get_multiple_rates("USD", ["COP", "EUR", "MXN", "ARS"])

    if "error" in result:
        await update.message.reply_text(f"Error: {result['error']}")
        return

    rates = result.get("rates", {})
    date = result.get("date", "N/A")

    text = f"""
💵 Tipo de cambio USD ({date})

🇨🇴 COP: ${rates.get('COP', 'N/A'):,.2f}
🇪🇺 EUR: €{rates.get('EUR', 'N/A'):.4f}
🇲🇽 MXN: ${rates.get('MXN', 'N/A'):,.2f}
🇦🇷 ARS: ${rates.get('ARS', 'N/A'):,.2f}
"""
    await update.message.reply_text(text)


async def euro_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Obteniendo tipo de cambio...")

    result = get_multiple_rates("EUR", ["COP", "USD", "MXN", "ARS"])

    if "error" in result:
        await update.message.reply_text(f"Error: {result['error']}")
        return

    rates = result.get("rates", {})
    date = result.get("date", "N/A")

    text = f"""
💶 Tipo de cambio EUR ({date})

🇨🇴 COP: ${rates.get('COP', 'N/A'):,.2f}
🇺🇸 USD: ${rates.get('USD', 'N/A'):.4f}
🇲🇽 MXN: ${rates.get('MXN', 'N/A'):,.2f}
🇦🇷 ARS: ${rates.get('ARS', 'N/A'):,.2f}
"""
    await update.message.reply_text(text)
