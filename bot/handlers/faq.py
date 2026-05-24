from telegram import Update
from telegram.ext import ContextTypes
from bot.data.faq_data import FAQ
from bot.data.messages import FAQ_INTRO
from bot.keyboards.inline import build_faq_keyboard, build_back_keyboard


async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = build_faq_keyboard()
    await update.message.reply_text(FAQ_INTRO, reply_markup=keyboard, parse_mode="Markdown")


async def faq_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    slug = query.data.split(":", 1)[1]

    if slug == "back":
        keyboard = build_faq_keyboard()
        await query.edit_message_text(FAQ_INTRO, reply_markup=keyboard, parse_mode="Markdown")
        return

    faq_item = FAQ.get(slug)
    if not faq_item:
        await query.edit_message_text("Вопрос не найден.")
        return

    text = (
        f"*{faq_item['question_ru']}*\n"
        f"_{faq_item['question_kz']}_\n\n"
        f"{faq_item['answer_ru']}\n\n"
        f"〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n"
        f"{faq_item['answer_kz']}"
    )

    await query.edit_message_text(
        text,
        reply_markup=build_back_keyboard(),
        parse_mode="Markdown",
    )
