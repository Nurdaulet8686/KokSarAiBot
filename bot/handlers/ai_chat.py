import io
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from bot.services.gemini import get_response, get_response_from_audio
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


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = context.user_data.get("lang", "ru")
    topic = context.user_data.get("topic")

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    try:
        voice = update.message.voice or update.message.audio
        file = await context.bot.get_file(voice.file_id)
        audio_bytes = await file.download_as_bytearray()

        response = await get_response_from_audio(
            audio_bytes=bytes(audio_bytes),
            lang=lang,
            topic=topic,
        )
    except Exception:
        response = None

    if response is None:
        await update.message.reply_text(MESSAGES[lang]["ai_error"])
    else:
        await update.message.reply_text(response)
