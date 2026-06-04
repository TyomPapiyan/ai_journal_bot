from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from google.genai import types
import asyncio
import json

from database import upsert_user, save_entry, update_entry_analysis, get_entries, get_entry_count
from ai import analyze_entry, format_analysis
from ai.analyzer import client, MODEL, SYSTEM_INSTRUCTION
from .keyboards import main_menu, cancel_keyboard, entries_inline

router = Router()


# ── FSM States ────────────────────────────────────────────────────────────

class JournalFSM(StatesGroup):
    waiting_for_entry = State()
    waiting_for_dialog = State()


# ── /start ────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    upsert_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    name = message.from_user.first_name or "друг"
    await message.answer(
        f"Привет, <b>{name}</b>! 👋\n\n"
        "Я твой личный AI-дневник. Пиши мне о своём дне, "
        "мыслях и переживаниях — я выслушаю и дам тёплый отклик.\n\n"
        "Выбери действие ниже 👇",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


# ── /restart ──────────────────────────────────────────────────────────────

@router.message(Command("restart"))
async def cmd_restart(message: Message, state: FSMContext):
    await state.clear()
    name = message.from_user.first_name or "друг"
    await message.answer(
        f"🔄 Перезапуск...\n\n"
        f"Привет снова, <b>{name}</b>! 👋\n"
        "Всё сброшено. Выбери действие 👇",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


# ── /end ──────────────────────────────────────────────────────────────────

@router.message(Command("end"))
@router.message(F.text == "👋 Завершить сессию")
async def cmd_end(message: Message, state: FSMContext):
    await state.clear()
    name = message.from_user.first_name or "друг"
    await message.answer(
        f"👋 До свидания, <b>{name}</b>!\n\n"
        "Спасибо, что доверяешь мне свои мысли. "
        "Возвращайся когда захочешь — я всегда здесь 🤗\n\n"
        "Чтобы начать снова, напиши /start",
        parse_mode="HTML",
    )


# ── /help ─────────────────────────────────────────────────────────────────

@router.message(Command("help"))
@router.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: Message):
    await message.answer(
        "<b>Как пользоваться дневником:</b>\n\n"
        "✍️ <b>Новая запись</b> — напиши о своём дне\n"
        "📖 <b>Мои записи</b> — посмотреть последние 10 записей\n"
        "📊 <b>Статистика</b> — сколько записей ты сделал\n\n"
        "После каждой записи AI проанализирует твоё настроение "
        "и даст психологическое наблюдение 🤖\n\n"
        "<b>Команды:</b>\n"
        "/start — начало\n"
        "/restart — перезапустить бота\n"
        "/end — завершить сессию\n"
        "/help — помощь",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# ── New entry ─────────────────────────────────────────────────────────────

@router.message(F.text == "✍️ Новая запись")
async def new_entry_start(message: Message, state: FSMContext):
    await state.set_state(JournalFSM.waiting_for_entry)
    await message.answer(
        "📝 Расскажи, как прошёл твой день или что у тебя на душе.\n"
        "Пиши свободно — всё останется только здесь.",
        reply_markup=cancel_keyboard(),
    )


@router.message(JournalFSM.waiting_for_entry, F.text == "❌ Отмена")
async def new_entry_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено.", reply_markup=main_menu())


@router.message(JournalFSM.waiting_for_entry, F.text)
async def new_entry_receive(message: Message, state: FSMContext):
    text = message.text.strip()

    entry_id = save_entry(message.from_user.id, text)

    thinking = await message.answer("🤔 Анализирую запись…")

    analysis = await analyze_entry(text)
    update_entry_analysis(entry_id, analysis["mood"], str(analysis))

    await thinking.delete()
    await state.set_state(JournalFSM.waiting_for_dialog)
    await state.update_data(dialog_history=[
        {"role": "user", "parts": [text]},
        {"role": "model", "parts": [format_analysis(analysis)]},
    ])
    await message.answer(
        "✅ <b>Запись сохранена!</b>\n\n" + format_analysis(analysis) +
        "\n\n<i>Можешь продолжить — я слушаю. Или нажми ❌ Отмена.</i>",
        parse_mode="HTML",
        reply_markup=cancel_keyboard(),
    )


# ── Dialog after entry ────────────────────────────────────────────────────

@router.message(JournalFSM.waiting_for_dialog, F.text == "❌ Отмена")
async def dialog_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Хорошо, возвращаемся в меню.", reply_markup=main_menu())


@router.message(JournalFSM.waiting_for_dialog, F.text)
async def dialog_continue(message: Message, state: FSMContext):
    data = await state.get_data()
    history = data.get("dialog_history", [])
    history.append({"role": "user", "parts": [message.text]})

    thinking = await message.answer("🤔 Думаю…")

    try:
        # Собираем историю в формат google.genai
        contents = [
            types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["parts"][0])]
            )
            for msg in history
        ]

        response = await asyncio.to_thread(
            client.models.generate_content,
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
            )
        )
        reply = response.text.strip()

        # убираем ```json если Gemini вернул JSON вместо текста
        if reply.startswith("```"):
            raw = reply.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            try:
                data_json = json.loads(raw.strip())
                reply = (
                    f"{data_json.get('emoji', '')} <b>Настроение:</b> {data_json.get('mood', '')}\n\n"
                    f"{data_json.get('summary', '')}\n\n"
                    f"{data_json.get('insight', '')}\n\n"
                    f"💭 <i>{data_json.get('question', '')}</i>"
                )
            except Exception:
                reply = raw.strip()

    except Exception as e:
        reply = "Прости, что-то пошло не так. Попробуй ещё раз."

    history.append({"role": "model", "parts": [reply]})
    await state.update_data(dialog_history=history)

    await thinking.delete()
    await message.answer(reply, parse_mode="HTML", reply_markup=cancel_keyboard())


# ── View entries ──────────────────────────────────────────────────────────

@router.message(F.text == "📖 Мои записи")
async def view_entries(message: Message):
    entries = get_entries(message.from_user.id, limit=10)
    if not entries:
        await message.answer("У тебя пока нет записей. Напиши первую! ✍️", reply_markup=main_menu())
        return
    await message.answer(
        "Вот твои последние записи. Нажми на любую, чтобы прочитать:",
        reply_markup=entries_inline(entries),
    )


@router.callback_query(F.data.startswith("entry:"))
async def show_entry(callback: CallbackQuery):
    entry_id = int(callback.data.split(":")[1])
    entries  = get_entries(callback.from_user.id, limit=50)
    entry    = next((e for e in entries if e["id"] == entry_id), None)

    if not entry:
        await callback.answer("Запись не найдена.", show_alert=True)
        return

    date_str = entry["created_at"][:16]
    mood     = entry["mood"] or "не определено"
    text     = (
        f"📅 <b>{date_str}</b>   |   Настроение: <b>{mood}</b>\n\n"
        f"{entry['content']}"
    )
    await callback.message.answer(text, parse_mode="HTML", reply_markup=main_menu())
    await callback.answer()


@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()


# ── Statistics ────────────────────────────────────────────────────────────

@router.message(F.text == "📊 Статистика")
async def statistics(message: Message):
    count = get_entry_count(message.from_user.id)
    entries = get_entries(message.from_user.id, limit=50)

    moods = {}
    for e in entries:
        if e["mood"]:
            moods[e["mood"]] = moods.get(e["mood"], 0) + 1

    mood_lines = "\n".join(
        f"  • {mood}: {cnt} раз" for mood, cnt in sorted(moods.items(), key=lambda x: -x[1])
    ) or "  Пока нет данных"

    await message.answer(
        f"<b>📊 Твоя статистика</b>\n\n"
        f"Всего записей: <b>{count}</b>\n\n"
        f"<b>Распределение настроений:</b>\n{mood_lines}",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# ── Fallback ──────────────────────────────────────────────────────────────

@router.message(F.text)
async def unknown_message(message: Message):
    await message.answer(
        "Выбери действие из меню 👇",
        reply_markup=main_menu(),
    )