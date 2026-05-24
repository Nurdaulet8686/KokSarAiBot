from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.data.faq_data import FAQ


def build_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇰🇿 Қазақша", callback_data="lang:kz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang:ru"),
        ]
    ])


def build_main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    if lang == "kz":
        buttons = [
            [InlineKeyboardButton("💬  WhatsApp-қа жазу", url=WHATSAPP_URL)],
            [
                InlineKeyboardButton("🌐 Сайт жасау", callback_data="topic:website"),
                InlineKeyboardButton("📱 Мобильді қосымша", callback_data="topic:mobile"),
            ],
            [
                InlineKeyboardButton("🤖 Telegram бот", callback_data="topic:bot"),
                InlineKeyboardButton("⚡ AI автоматтандыру", callback_data="topic:ai"),
            ],
            [InlineKeyboardButton("🖥  Компьютер және ноутбук ремонт", callback_data="topic:repair")],
            [
                InlineKeyboardButton("❓ Жиі сұрақтар", callback_data="topic:faq"),
                InlineKeyboardButton("📞 Байланыс", callback_data="topic:contact"),
            ],
            [InlineKeyboardButton("🌐  Тілді өзгерту", callback_data="change_lang")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton("💬  Написать в WhatsApp", url=WHATSAPP_URL)],
            [
                InlineKeyboardButton("🌐 Создание сайта", callback_data="topic:website"),
                InlineKeyboardButton("📱 Мобильное приложение", callback_data="topic:mobile"),
            ],
            [
                InlineKeyboardButton("🤖 Telegram-бот", callback_data="topic:bot"),
                InlineKeyboardButton("⚡ AI-автоматизация", callback_data="topic:ai"),
            ],
            [InlineKeyboardButton("🖥  Ремонт компьютеров и ноутбуков", callback_data="topic:repair")],
            [
                InlineKeyboardButton("❓ FAQ", callback_data="topic:faq"),
                InlineKeyboardButton("📞 Контакты", callback_data="topic:contact"),
            ],
            [InlineKeyboardButton("🌐  Сменить язык", callback_data="change_lang")],
        ]
    return InlineKeyboardMarkup(buttons)


WHATSAPP_URL = "https://wa.me/77001667186"


def build_back_to_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    label = "⬅️ Басты мәзір" if lang == "kz" else "⬅️ Главное меню"
    wa_label = "💬 WhatsApp-қа жазу" if lang == "kz" else "💬 Написать в WhatsApp"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(wa_label, url=WHATSAPP_URL)],
        [InlineKeyboardButton(label, callback_data="back_menu")],
    ])


def build_contact_keyboard(lang: str) -> InlineKeyboardMarkup:
    wa_label = "💬 WhatsApp-қа жазу" if lang == "kz" else "💬 Написать в WhatsApp"
    menu_label = "⬅️ Басты мәзір" if lang == "kz" else "⬅️ Главное меню"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(wa_label, url=WHATSAPP_URL)],
        [InlineKeyboardButton(menu_label, callback_data="back_menu")],
    ])


def build_faq_keyboard(lang: str) -> InlineKeyboardMarkup:
    key = "question_kz" if lang == "kz" else "question_ru"
    buttons = [
        [InlineKeyboardButton(text=data[key], callback_data=f"faq:{slug}")]
        for slug, data in FAQ.items()
    ]
    back_label = "⬅️ Басты мәзір" if lang == "kz" else "⬅️ Главное меню"
    buttons.append([InlineKeyboardButton(back_label, callback_data="back_menu")])
    return InlineKeyboardMarkup(buttons)


def build_back_faq_keyboard(lang: str) -> InlineKeyboardMarkup:
    faq_label = "⬅️ FAQ-қа оралу" if lang == "kz" else "⬅️ Назад к FAQ"
    menu_label = "⬅️ Басты мәзір" if lang == "kz" else "⬅️ Главное меню"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(faq_label, callback_data="topic:faq")],
        [InlineKeyboardButton(menu_label, callback_data="back_menu")],
    ])
