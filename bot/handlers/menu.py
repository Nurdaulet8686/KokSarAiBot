from html import escape
from telegram import Update
from telegram.ext import ContextTypes
from bot.data.faq_data import FAQ
from bot.data.messages import MESSAGES
from bot.keyboards.inline import (
    build_language_keyboard,
    build_main_menu_keyboard,
    build_faq_keyboard,
    build_back_faq_keyboard,
    build_back_to_menu_keyboard,
    build_contact_keyboard,
)

TOPIC_KEYS = {
    "website": "topic_website",
    "mobile": "topic_mobile",
    "ai": "topic_ai",
    "bot": "topic_bot",
    "repair": "topic_repair",
    "contact": "contact",
}


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    lang = query.data.split(":", 1)[1]
    context.user_data["lang"] = lang
    context.user_data.pop("topic", None)

    await query.edit_message_text(
        MESSAGES[lang]["welcome"],
        parse_mode="HTML",
        reply_markup=build_main_menu_keyboard(lang),
    )


async def topic_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "ru")
    topic = query.data.split(":", 1)[1]
    context.user_data["topic"] = topic

    if topic == "faq":
        await query.edit_message_text(
            MESSAGES[lang]["faq_intro"],
            parse_mode="HTML",
            reply_markup=build_faq_keyboard(lang),
        )
        return

    msg_key = TOPIC_KEYS.get(topic)
    if not msg_key:
        return

    keyboard = build_contact_keyboard(lang) if topic == "contact" else build_back_to_menu_keyboard(lang)

    await query.edit_message_text(
        MESSAGES[lang][msg_key],
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def faq_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "ru")
    slug = query.data.split(":", 1)[1]

    faq_item = FAQ.get(slug)
    if not faq_item:
        return

    if lang == "kz":
        text = (
            f"<b>{escape(faq_item['question_kz'])}</b>\n\n"
            f"{escape(faq_item['answer_kz'])}\n\n"
            f"〰〰〰〰〰〰〰〰〰〰\n\n"
            f"<i>{escape(faq_item['question_ru'])}</i>\n\n"
            f"{escape(faq_item['answer_ru'])}"
        )
    else:
        text = (
            f"<b>{escape(faq_item['question_ru'])}</b>\n\n"
            f"{escape(faq_item['answer_ru'])}\n\n"
            f"〰〰〰〰〰〰〰〰〰〰\n\n"
            f"<i>{escape(faq_item['question_kz'])}</i>\n\n"
            f"{escape(faq_item['answer_kz'])}"
        )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=build_back_faq_keyboard(lang),
    )


async def back_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "ru")
    context.user_data.pop("topic", None)

    await query.edit_message_text(
        MESSAGES[lang]["choose_topic"],
        parse_mode="HTML",
        reply_markup=build_main_menu_keyboard(lang),
    )


async def change_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    context.user_data.pop("lang", None)
    context.user_data.pop("topic", None)

    await query.edit_message_text(
        "🇰🇿 Тілді таңдаңыз / 🇷🇺 Выберите язык:",
        reply_markup=build_language_keyboard(),
    )
