import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from config import TELEGRAM_BOT_TOKEN, LOG_LEVEL
from bot.handlers.commands import start, help_command, services, contact, faq_command
from bot.handlers.menu import (
    language_callback,
    topic_callback,
    faq_callback,
    back_menu_callback,
    change_lang_callback,
)
from bot.handlers.ai_chat import handle_message, handle_voice

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
)
logger = logging.getLogger(__name__)


def main() -> None:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("faq", faq_command))
    app.add_handler(CommandHandler("services", services))
    app.add_handler(CommandHandler("contact", contact))

    app.add_handler(CallbackQueryHandler(language_callback, pattern=r"^lang:"))
    app.add_handler(CallbackQueryHandler(topic_callback, pattern=r"^topic:"))
    app.add_handler(CallbackQueryHandler(faq_callback, pattern=r"^faq:"))
    app.add_handler(CallbackQueryHandler(back_menu_callback, pattern=r"^back_menu$"))
    app.add_handler(CallbackQueryHandler(change_lang_callback, pattern=r"^change_lang$"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))

    logger.info("KokSarAi bot started.")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
