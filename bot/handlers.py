from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramForbiddenError
from google.genai import types
import asyncio
import json

from database import upsert_user, save_entry, update_entry_analysis, get_entries, get_entry_count, set_user_language, get_user_language
from ai import analyze_entry, format_analysis
from ai.analyzer import client, MODEL, SYSTEM_INSTRUCTIONS
from .keyboards import main_menu, cancel_keyboard, entries_inline, language_keyboard, TEXTS

router = Router()

MESSAGES = {
    "ru": {
        "choose_lang": "Привет! 👋 Выбери язык / Choose language / Ընտրիր լեզուն",
        "welcome": "Привет, <b>{name}</b>! 👋\n\nЯ твой личный AI-дневник. Пиши мне о своём дне, мыслях и переживаниях — я выслушаю и дам тёплый отклик.\n\nВыбери действие ниже 👇",
        "restart": "🔄 Перезапуск...\n\nПривет снова, <b>{name}</b>! 👋\nВсё сброшено. Выбери действие 👇",
        "end": "👋 До свидания, <b>{name}</b>!\n\nСпасибо, что доверяешь мне свои мысли. Возвращайся когда захочешь — я всегда здесь 🤗\n\nЧтобы начать снова, напиши /start",
        "help": "<b>Как пользоваться дневником:</b>\n\n✍️ <b>Новая запись</b> — напиши о своём дне\n📖 <b>Мои записи</b> — посмотреть последние 10 записей\n📊 <b>Статистика</b> — сколько записей ты сделал\n\n<b>Команды:</b>\n/start — начало\n/restart — перезапустить\n/end — завершить сессию\n/help — помощь",
        "new_entry_prompt": "📝 Расскажи, как прошёл твой день или что у тебя на душе.\nПиши свободно — всё останется только здесь.",
        "cancelled": "Отменено.",
        "thinking": "🤔 Анализирую запись…",
        "thinking2": "🤔 Думаю…",
        "saved": "✅ <b>Запись сохранена!</b>\n\n{analysis}\n\n<i>Можешь продолжить — я слушаю. Или нажми ❌ Отмена.</i>",
        "back_menu": "Хорошо, возвращаемся в меню.",
        "no_entries": "У тебя пока нет записей. Напиши первую! ✍️",
        "entries_header": "Вот твои последние записи. Нажми на любую, чтобы прочитать:",
        "entry_not_found": "Запись не найдена.",
        "stats": "<b>📊 Твоя статистика</b>\n\nВсего записей: <b>{count}</b>\n\n<b>Распределение настроений:</b>\n{moods}",
        "no_mood_data": "Пока нет данных",
        "fallback": "Выбери действие из меню 👇",
        "error": "Прости, что-то пошло не так. Попробуй ещё раз.",
        "lang_changed": "✅ Язык изменён на Русский 🇷🇺",
    },
    "hy": {
        "choose_lang": "Բարև! 👋 Ընտրիր լեզուն / Choose language / Выбери язык",
        "welcome": "Բարև, <b>{name}</b>! 👋\n\nԵս քո անձնական AI-օրագիրն եմ։ Գրիր ինձ քո օրվա, մտքերի ու զգացմունքների մասին — ես կլսեմ և ջերմ արձագանք կտամ։\n\nԸնտրիր գործողություն 👇",
        "restart": "🔄 Վերագործարկում...\n\nԲարև նորից, <b>{name}</b>! 👋\nԱմեն ինչ վերականգնված է։ Ընտրիր գործողություն 👇",
        "end": "👋 Ցտեսություն, <b>{name}</b>!\n\nՇնորհակալ եմ, որ կիսվում ես ինձ հետ։ Վերադարձիր երբ ցանկանաս 🤗\n\nՆորից սկսելու համար գրիր /start",
        "help": "<b>Ինչպես օգտագործել օրագիրը.</b>\n\n✍️ <b>Նոր գրառում</b> — գրիր քո օրվա մասին\n📖 <b>Իմ գրառումները</b> — տես վերջին 10 գրառումները\n📊 <b>Վիճակագրություն</b> — քանի գրառում ես արել\n\n<b>Հրամաններ.</b>\n/start — սկիզբ\n/restart — վերագործարկել\n/end — ավարտել նիստը\n/help — օգնություն",
        "new_entry_prompt": "📝 Պատմիր, թե ինչպես անցավ օրդ կամ ինչ կա հոգուդ վրա։\nԳրիր ազատ — ամեն ինչ կմնա միայն այստեղ։",
        "cancelled": "Չեղարկված է։",
        "thinking": "🤔 Վերլուծում եմ գրառումը…",
        "thinking2": "🤔 Մտածում եմ…",
        "saved": "✅ <b>Գրառումը պահպանված է!</b>\n\n{analysis}\n\n<i>Կարող ես շարունակել — ես լսում եմ։ Կամ սեղմիր ❌ Չեղարկել։</i>",
        "back_menu": "Լավ, վերադառնում ենք մենյու։",
        "no_entries": "Դու դեռ գրառումներ չունես։ Գրիր առաջինը! ✍️",
        "entries_header": "Ահա քո վերջին գրառումները։ Սեղմիր որևէ մեկի վրա՝ կարդալու համար.",
        "entry_not_found": "Գրառումը չի գտնվել։",
        "stats": "<b>📊 Քո վիճակագրությունը</b>\n\nԸնդամենը գրառում. <b>{count}</b>\n\n<b>Տրամադրությունների բաշխում.</b>\n{moods}",
        "no_mood_data": "Տվյալներ դեռ չկան",
        "fallback": "Ընտրիր գործողություն մենյուից 👇",
        "error": "Կներիր, ինչ-որ բան սխալ գնաց։ Փորձիր նորից։",
        "lang_changed": "✅ Լեզուն փոխված է Հայերենի 🇦🇲",
    },
    "en": {
        "choose_lang": "Hi! 👋 Choose language / Выбери язык / Ընտրիր լեզուն",
        "welcome": "Hi, <b>{name}</b>! 👋\n\nI'm your personal AI journal. Write to me about your day, thoughts and feelings — I'll listen and give a warm response.\n\nChoose an action below 👇",
        "restart": "🔄 Restarting...\n\nHi again, <b>{name}</b>! 👋\nEverything is reset. Choose an action 👇",
        "end": "👋 Goodbye, <b>{name}</b>!\n\nThank you for trusting me with your thoughts. Come back whenever you want 🤗\n\nTo start again, type /start",
        "help": "<b>How to use the journal:</b>\n\n✍️ <b>New Entry</b> — write about your day\n📖 <b>My Entries</b> — view last 10 entries\n📊 <b>Statistics</b> — how many entries you've made\n\n<b>Commands:</b>\n/start — start\n/restart — restart bot\n/end — end session\n/help — help",
        "new_entry_prompt": "📝 Tell me how your day went or what's on your mind.\nWrite freely — everything stays here.",
        "cancelled": "Cancelled.",
        "thinking": "🤔 Analyzing entry…",
        "thinking2": "🤔 Thinking…",
        "saved": "✅ <b>Entry saved!</b>\n\n{analysis}\n\n<i>You can continue — I'm listening. Or press ❌ Cancel.</i>",
        "back_menu": "Ok, going back to menu.",
        "no_entries": "You have no entries yet. Write your first one! ✍️",
        "entries_header": "Here are your recent entries. Tap any to read:",
        "entry_not_found": "Entry not found.",
        "stats": "<b>📊 Your Statistics</b>\n\nTotal entries: <b>{count}</b>\n\n<b>Mood distribution:</b>\n{moods}",
        "no_mood_data": "No data yet",
        "fallback": "Choose an action from the menu 👇",
        "error": "Sorry, something went wrong. Please try again.",
        "lang_changed": "✅ Language changed to English 🇬🇧",
    },
}

def get_msg(lang: str, key: str) -> str:
    return MESSAGES.get(lang, MESSAGES["ru"]).get(key, "")

class JournalFSM(StatesGroup):
    waiting_for_entry = State()
    waiting_for_dialog = State()

def is_cancel(text: str) -> bool:
    return text in ["❌ Отмена", "❌ Չեղարկել", "❌ Cancel"]

def is_end(text: str) -> bool:
    return text in ["👋 Завершить сессию", "👋 Ավարտել նիստը", "👋 End Session"]

def is_help(text: str) -> bool:
    return text in ["ℹ️ Помощь", "ℹ️ Օгнություն", "ℹ️ Help", "ℹ️ Օгնություն"]

def is_new_entry(text: str) -> bool:
    return text in ["✍️ Новая запись", "✍️ Նոր գրառում", "✍️ New Entry"]

def is_my_entries(text: str) -> bool:
    return text in ["📖 Мои записи", "📖 Իմ գրառումները", "📖 My Entries"]

def is_stats(text: str) -> bool:
    return text in ["📊 Статистика", "📊 Վիճակагрություն", "📊 Statistics", "📊 Վիճakագрություն"]

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    upsert_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    lang = get_user_language(message.from_user.id)
    await message.answer(
        get_msg(lang, "choose_lang"),
        reply_markup=language_keyboard(),
    )

@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split(":")[1]
    set_user_language(callback.from_user.id, lang)
    name = callback.from_user.first_name or "друг"
    await callback.message.delete()
    await callback.message.answer(
        get_msg(lang, "welcome").format(name=name),
        reply_markup=main_menu(lang),
        parse_mode="HTML",
    )
    await callback.answer()

@router.message(Command("restart"))
async def cmd_restart(message: Message, state: FSMContext):
    await state.clear()
    lang = get_user_language(message.from_user.id)
    name = message.from_user.first_name or "друг"
    await message.answer(
        get_msg(lang, "restart").format(name=name),
        reply_markup=main_menu(lang),
        parse_mode="HTML",
    )

@router.message(Command("end"))
async def cmd_end_command(message: Message, state: FSMContext):
    await state.clear()
    lang = get_user_language(message.from_user.id)
    name = message.from_user.first_name or "друг"
    await message.answer(get_msg(lang, "end").format(name=name), parse_mode="HTML")

@router.message(F.text.func(is_end))
async def cmd_end(message: Message, state: FSMContext):
    await state.clear()
    lang = get_user_language(message.from_user.id)
    name = message.from_user.first_name or "друг"
    await message.answer(get_msg(lang, "end").format(name=name), parse_mode="HTML")

@router.message(Command("help"))
async def cmd_help_command(message: Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_msg(lang, "help"), parse_mode="HTML", reply_markup=main_menu(lang))

@router.message(F.text.func(is_help))
async def cmd_help(message: Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_msg(lang, "help"), parse_mode="HTML", reply_markup=main_menu(lang))

@router.message(F.text.func(is_new_entry))
async def new_entry_start(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await state.set_state(JournalFSM.waiting_for_entry)
    await message.answer(get_msg(lang, "new_entry_prompt"), reply_markup=cancel_keyboard(lang))

@router.message(JournalFSM.waiting_for_entry, F.text.func(is_cancel))
async def new_entry_cancel(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await state.clear()
    await message.answer(get_msg(lang, "cancelled"), reply_markup=main_menu(lang))

@router.message(JournalFSM.waiting_for_entry, F.text)
async def new_entry_receive(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    text = message.text.strip()
    entry_id = save_entry(message.from_user.id, text)
    thinking = await message.answer(get_msg(lang, "thinking"))
    analysis = await analyze_entry(text, lang)
    update_entry_analysis(entry_id, analysis["mood"], str(analysis))
    await thinking.delete()
    await state.set_state(JournalFSM.waiting_for_dialog)
    from ai.analyzer import format_analysis
    formatted = format_analysis(analysis, lang)
    await state.update_data(dialog_history=[
        {"role": "user", "parts": [text]},
        {"role": "model", "parts": [formatted]},
    ], lang=lang)
    await message.answer(
        get_msg(lang, "saved").format(analysis=formatted),
        parse_mode="HTML",
        reply_markup=cancel_keyboard(lang),
    )

@router.message(JournalFSM.waiting_for_dialog, F.text.func(is_cancel))
async def dialog_cancel(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await state.clear()
    await message.answer(get_msg(lang, "back_menu"), reply_markup=main_menu(lang))

@router.message(JournalFSM.waiting_for_dialog, F.text)
async def dialog_continue(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", get_user_language(message.from_user.id))
    history = data.get("dialog_history", [])
    history.append({"role": "user", "parts": [message.text]})
    thinking = await message.answer(get_msg(lang, "thinking2"))
    try:
        contents = [
            types.Content(role=msg["role"], parts=[types.Part(text=msg["parts"][0])])
            for msg in history
        ]
        from ai.analyzer import SYSTEM_INSTRUCTIONS
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTIONS.get(lang, SYSTEM_INSTRUCTIONS["ru"]))
        )
        reply = response.text.strip()
        if reply.startswith("```"):
            raw = reply.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            try:
                from ai.analyzer import format_analysis
                data_json = json.loads(raw.strip())
                reply = format_analysis(data_json, lang)
            except Exception:
                reply = raw.strip()
    except Exception:
        reply = get_msg(lang, "error")
    history.append({"role": "model", "parts": [reply]})
    await state.update_data(dialog_history=history)
    await thinking.delete()
    await message.answer(reply, parse_mode="HTML", reply_markup=cancel_keyboard(lang))

@router.message(F.text.func(is_my_entries))
async def view_entries(message: Message):
    lang = get_user_language(message.from_user.id)
    entries = get_entries(message.from_user.id, limit=10)
    if not entries:
        await message.answer(get_msg(lang, "no_entries"), reply_markup=main_menu(lang))
        return
    await message.answer(get_msg(lang, "entries_header"), reply_markup=entries_inline(entries, lang))

@router.callback_query(F.data.startswith("entry:"))
async def show_entry(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    entry_id = int(callback.data.split(":")[1])
    entries = get_entries(callback.from_user.id, limit=50)
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if not entry:
        await callback.answer(get_msg(lang, "entry_not_found"), show_alert=True)
        return
    date_str = entry["created_at"][:16]
    mood = entry["mood"] or "—"
    text = f"📅 <b>{date_str}</b>   |   {mood}\n\n{entry['content']}"
    await callback.message.answer(text, parse_mode="HTML", reply_markup=main_menu(lang))
    await callback.answer()

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

@router.message(F.text.func(is_stats))
async def statistics(message: Message):
    lang = get_user_language(message.from_user.id)
    count = get_entry_count(message.from_user.id)
    entries = get_entries(message.from_user.id, limit=50)
    moods = {}
    for e in entries:
        if e["mood"]:
            moods[e["mood"]] = moods.get(e["mood"], 0) + 1
    mood_lines = "\n".join(
        f"  • {mood}: {cnt}" for mood, cnt in sorted(moods.items(), key=lambda x: -x[1])
    ) or get_msg(lang, "no_mood_data")
    await message.answer(
        get_msg(lang, "stats").format(count=count, moods=mood_lines),
        parse_mode="HTML",
        reply_markup=main_menu(lang),
    )

@router.message(F.text)
async def unknown_message(message: Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_msg(lang, "fallback"), reply_markup=main_menu(lang))

@router.error()

@router.error()
async def error_handler(event) -> bool:
    if isinstance(event.exception, TelegramForbiddenError):
        return True
    return False
