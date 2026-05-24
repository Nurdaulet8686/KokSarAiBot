from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.inline import build_language_keyboard, build_main_menu_keyboard, build_faq_keyboard, build_contact_keyboard
from bot.data.messages import MESSAGES

_S = " "  # non-breaking space


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("lang", None)
    context.user_data.pop("topic", None)
    await update.message.reply_text(
        f"{'✦' + ' ━' * 16 + ' ✦'}\n\n"
        f"🤖{_S*4}K o k S a r A i{_S*4}🤖\n\n"
        f"{'✦' + ' ━' * 16 + ' ✦'}\n\n"
        f"🇰🇿{_S*3}Тілді таңдаңыз\n"
        f"🇷🇺{_S*3}Выберите язык 👇",
        parse_mode="HTML",
        reply_markup=build_language_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = context.user_data.get("lang", "ru")
    await update.message.reply_text(MESSAGES[lang]["help"], parse_mode="HTML")


async def services(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = context.user_data.get("lang", "ru")
    await update.message.reply_text(
        MESSAGES[lang]["services"],
        parse_mode="HTML",
        reply_markup=build_main_menu_keyboard(lang),
    )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = context.user_data.get("lang", "ru")
    await update.message.reply_text(
        MESSAGES[lang]["contact"],
        parse_mode="HTML",
        reply_markup=build_contact_keyboard(lang),
    )


async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = context.user_data.get("lang", "ru")
    await update.message.reply_text(
        MESSAGES[lang]["faq_intro"],
        parse_mode="HTML",
        reply_markup=build_faq_keyboard(lang),
    )
