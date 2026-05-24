from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from bot.services.gemini import get_response
from bot.data.messages import MESSAGES


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = context.user_data.get("lang", "ru")
    topic = context.user_data.get("topic")

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    response = await get_response(update.message.text, lang=lang, topic=topic)

    if response is None:
        await update.message.reply_text(MESSAGES[lang]["ai_error"])
    else:
        await update.message.reply_text(response)
