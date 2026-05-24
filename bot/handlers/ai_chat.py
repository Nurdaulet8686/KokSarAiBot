from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from bot.services.gemini import get_response, get_response_from_audio
from bot.data.messages import MESSAGES
from bot.keyboards.inline import build_ai_response_keyboard


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
        await update.message.reply_text(
            response,
            reply_markup=build_ai_response_keyboard(lang),
        )


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = context.user_data.get("lang", "ru")

    no_audio_msg = {
        "kz": "🎤 Дауыстық хабарларды өңдеу уақытша қолжетімді емес. Мәтін арқылы жазыңыз немесе: @koksarai_support",
        "ru": "🎤 Обработка голосовых сообщений временно недоступна. Напишите текстом или: @koksarai_support",
    }
    await update.message.reply_text(
        no_audio_msg.get(lang, no_audio_msg["ru"]),
        reply_markup=build_ai_response_keyboard(lang),
    )
