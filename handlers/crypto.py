from telegram import Update
from telegram.ext import ContextTypes
from services.crypto_api import get_top_coins, get_coin_price


async def crypto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await coin_command(update, context)
        return

    await update.message.reply_text("Obteniendo top 10 criptomonedas...")

    coins = get_top_coins(10)

    if not coins or "error" in coins[0]:
        await update.message.reply_text("Error al obtener datos de criptomonedas")
        return

    text = "🪙 Top 10 Criptomonedas\n\n"

    for i, coin in enumerate(coins, 1):
        name = coin.get("name", "N/A")
        symbol = coin.get("symbol", "N/A").upper()
        price = coin.get("current_price", 0)
        change = coin.get("price_change_percentage_24h", 0)

        emoji = "🟢" if change >= 0 else "🔴"
        text += f"{i}. {name} ({symbol})\n"
        text += f"   ${price:,.2f} {emoji} {change:+.2f}%\n\n"

    await update.message.reply_text(text)


async def coin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /crypto <nombre>\nEjemplo: /crypto bitcoin")
        return

    coin_id = context.args[0].lower()

    await update.message.reply_text(f"Obteniendo precio de {coin_id}...")

    result = get_coin_price(coin_id)

    if "error" in result:
        await update.message.reply_text(f"Error: {result['error']}")
        return

    price = result.get("price_usd", 0)
    change = result.get("change_24h", 0)
    market_cap = result.get("market_cap", 0)

    emoji = "🟢" if change >= 0 else "🔴"

    text = f"""
🪙 {coin_id.upper()}

Precio: ${price:,.2f}
Cambio 24h: {emoji} {change:+.2f}%
Market Cap: ${market_cap:,.0f}
"""
    await update.message.reply_text(text)
