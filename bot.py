import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
from config import TELEGRAM_TOKEN
from handlers.start import start_command, help_command
from handlers.weather import weather_command
from handlers.exchange import dollar_command, euro_command
from handlers.crypto import crypto_command
from handlers.news import news_command, tech_command
from handlers.convert import convert_command

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN no configurado")
        print("Crea un archivo .env con tu token de BotFather")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("ayuda", help_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clima", weather_command))
    app.add_handler(CommandHandler("dolar", dollar_command))
    app.add_handler(CommandHandler("euro", euro_command))
    app.add_handler(CommandHandler("crypto", crypto_command))
    app.add_handler(CommandHandler("noticias", news_command))
    app.add_handler(CommandHandler("tech", tech_command))
    app.add_handler(CommandHandler("convertir", convert_command))
    app.add_handler(CommandHandler("convert", convert_command))

    async def unknown(update, context):
        await update.message.reply_text(
            "Comando no reconocido. Usa /ayuda para ver los comandos disponibles."
        )

    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("Bot iniciado. Presiona Ctrl+C para detener.")
    app.run_polling()


if __name__ == "__main__":
    main()
