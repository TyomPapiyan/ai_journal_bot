import os
import json
import asyncio
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"
MAX_RETRIES = 3
RETRY_DELAY = 5

SYSTEM_INSTRUCTIONS = {
    "ru": """Ты — добросердечный AI-психолог и личный дневник-ассистент.
Твоя задача — анализировать записи пользователя и давать короткий, тёплый отклик.
Отвечай ТОЛЬКО валидным JSON (без markdown-блоков) в следующем формате:
{
  "mood": "<одно слово на русском: радость/грусть/тревога/спокойствие/злость/усталость/воодушевление/нейтральное>",
  "emoji": "<один подходящий эмодзи>",
  "summary": "<1-2 предложения на русском>",
  "insight": "<1-2 предложения на русском>",
  "question": "<один открытый вопрос на русском>"
}""",
    "hy": """Դու բարի AI-հոգեբան և անձնական օրագիր-օգնական ես։
Վերլուծիր օգտատիրոջ գրառումը և տուր կարճ, ջերմ արձագանք։
Պատասխանիր ՄԻԱՅՆ վավեր JSON-ով (առանց markdown) հետևյալ ձևաչափով.
{
  "mood": "<մեկ բառ հայերեն: ուրախություն/տխրություն/անհանգստություն/հանգստություն/բարկություն/հոգնածություն/ոգեշնչում/չեզոք>",
  "emoji": "<մեկ հարմար էմոջի>",
  "summary": "<1-2 նախադասություն հայերեն>",
  "insight": "<1-2 նախադասություն հայերեն>",
  "question": "<մեկ բաց հարց հայերեն>"
}""",
    "en": """You are a kind AI psychologist and personal journal assistant.
Analyze the user's entry and give a short, warm response.
Reply ONLY with valid JSON (no markdown) in this format:
{
  "mood": "<one word in English: joy/sadness/anxiety/calm/anger/fatigue/inspiration/neutral>",
  "emoji": "<one appropriate emoji>",
  "summary": "<1-2 sentences in English>",
  "insight": "<1-2 sentences in English>",
  "question": "<one open question in English>"
}""",
}

SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTIONS["ru"]

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def analyze_entry(text: str, lang: str = "ru") -> dict:
    system = SYSTEM_INSTRUCTIONS.get(lang, SYSTEM_INSTRUCTIONS["ru"])
    last_error = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=MODEL,
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=system,
                )
            )
            raw = response.text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw.strip())
        except json.JSONDecodeError:
            return _fallback(lang)
        except Exception as e:
            last_error = str(e)
            if ("429" in last_error or "quota" in last_error.lower()) and attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY * attempt)
                continue
            break
    return _fallback(lang)

def _fallback(lang: str = "ru") -> dict:
    fallbacks = {
        "ru": {"mood": "нейтральное", "emoji": "📝", "summary": "Запись сохранена.", "insight": "Анализ временно недоступен.", "question": "Как ты себя чувствуешь прямо сейчас?"},
        "hy": {"mood": "չեզոք", "emoji": "📝", "summary": "Գրառումը պահպանված է։", "insight": "Վերլուծությունը ժամանակավորապես անհասանելի է։", "question": "Ինչպե՞ս ես քեզ հիմա զգում։"},
        "en": {"mood": "neutral", "emoji": "📝", "summary": "Entry saved.", "insight": "Analysis temporarily unavailable.", "question": "How are you feeling right now?"},
    }
    return fallbacks.get(lang, fallbacks["ru"])

def format_analysis(analysis: dict, lang: str = "ru") -> str:
    labels = {
        "ru": ("Настроение", "Краткое резюме", "Наблюдение"),
        "hy": ("Տրամադրություն", "Կարճ ամփոփում", "Դիտարկում"),
        "en": ("Mood", "Summary", "Insight"),
    }
    l = labels.get(lang, labels["ru"])
    return (
        f"{analysis['emoji']} <b>{l[0]}:</b> {analysis['mood']}\n\n"
        f"<b>{l[1]}:</b>\n{analysis['summary']}\n\n"
        f"<b>{l[2]}:</b>\n{analysis['insight']}\n\n"
        f"💭 <i>{analysis['question']}</i>"
    )
