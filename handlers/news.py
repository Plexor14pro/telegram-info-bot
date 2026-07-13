from telegram import Update
from telegram.ext import ContextTypes
from services.news_api import get_general_news, get_tech_news


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Obteniendo últimas noticias...")

    articles = get_general_news(5)

    if not articles or "error" in articles[0]:
        await update.message.reply_text("Error al obtener noticias. Verifica tu NEWS_API_KEY.")
        return

    text = "📰 Últimas Noticias\n\n"

    for i, article in enumerate(articles, 1):
        title = article.get("title", "Sin título")
        source = article.get("source", "Fuente desconocida")
        text += f"{i}. {title}\n   Fuente: {source}\n\n"

    await update.message.reply_text(text)


async def tech_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Obteniendo noticias de tecnología...")

    articles = get_tech_news(5)

    if not articles or "error" in articles[0]:
        await update.message.reply_text("Error al obtener noticias de tecnología")
        return

    text = "💻 Noticias de Tecnología\n\n"

    for i, article in enumerate(articles, 1):
        title = article.get("title", "Sin título")
        summary = article.get("summary", "Sin resumen")
        source = article.get("source", "Fuente desconocida")
        text += f"{i}. {title}\n   {summary}\n   Fuente: {source}\n\n"

    await update.message.reply_text(text)
