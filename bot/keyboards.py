from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="✍️ Новая запись"),
        KeyboardButton(text="📖 Мои записи"),
    )
    builder.row(
        KeyboardButton(text="📊 Статистика"),
        KeyboardButton(text="ℹ️ Помощь"),
    )
    builder.row(
        KeyboardButton(text="👋 Завершить сессию"),
    )
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❌ Отмена"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def entries_inline(entries) -> InlineKeyboardMarkup:
    """Build an inline keyboard listing recent entries."""
    builder = InlineKeyboardBuilder()
    for entry in entries:
        created = entry["created_at"][:16]          # "YYYY-MM-DD HH:MM"
        mood    = entry["mood"] or "—"
        label   = f"{created}  |  {mood}"
        builder.row(InlineKeyboardButton(
            text=label,
            callback_data=f"entry:{entry['id']}"
        ))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_main"))
    return builder.as_markup()