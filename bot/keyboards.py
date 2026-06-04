from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

TEXTS = {
    "ru": {
        "new_entry": "✍️ Новая запись",
        "my_entries": "📖 Мои записи",
        "stats": "📊 Статистика",
        "help": "ℹ️ Помощь",
        "end": "👋 Завершить сессию",
        "cancel": "❌ Отмена",
        "back": "🔙 Назад",
    },
    "hy": {
        "new_entry": "✍️ Նոր գրառում",
        "my_entries": "📖 Իմ գրառումները",
        "stats": "📊 Վիճակագրություն",
        "help": "ℹ️ Օգնություն",
        "end": "👋 Ավարտել նիստը",
        "cancel": "❌ Չեղարկել",
        "back": "🔙 Հետ",
    },
    "en": {
        "new_entry": "✍️ New Entry",
        "my_entries": "📖 My Entries",
        "stats": "📊 Statistics",
        "help": "ℹ️ Help",
        "end": "👋 End Session",
        "cancel": "❌ Cancel",
        "back": "🔙 Back",
    },
}

def language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        InlineKeyboardButton(text="🇦🇲 Հայերեն", callback_data="lang:hy"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
    )
    return builder.as_markup()

def main_menu(lang: str = "ru") -> ReplyKeyboardMarkup:
    t = TEXTS.get(lang, TEXTS["ru"])
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=t["new_entry"]),
        KeyboardButton(text=t["my_entries"]),
    )
    builder.row(
        KeyboardButton(text=t["stats"]),
        KeyboardButton(text=t["help"]),
    )
    builder.row(
        KeyboardButton(text=t["end"]),
    )
    return builder.as_markup(resize_keyboard=True)

def cancel_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    t = TEXTS.get(lang, TEXTS["ru"])
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=t["cancel"]))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def entries_inline(entries, lang: str = "ru") -> InlineKeyboardMarkup:
    t = TEXTS.get(lang, TEXTS["ru"])
    builder = InlineKeyboardBuilder()
    for entry in entries:
        created = entry["created_at"][:16]
        mood = entry["mood"] or "—"
        label = f"{created}  |  {mood}"
        builder.row(InlineKeyboardButton(
            text=label,
            callback_data=f"entry:{entry['id']}"
        ))
    builder.row(InlineKeyboardButton(text=t["back"], callback_data="back_main"))
    return builder.as_markup()
