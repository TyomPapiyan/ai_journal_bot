import os
import json
import asyncio
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"
MAX_RETRIES = 3
RETRY_DELAY = 5

SYSTEM_INSTRUCTION = """Ты — добросердечный AI-психолог и личный дневник-ассистент.
Твоя задача — анализировать записи пользователя и давать короткий, тёплый отклик.

Отвечай ТОЛЬКО валидным JSON (без markdown-блоков) в следующем формате:
{
  "mood": "<одно слово на русском: радость/грусть/тревога/спокойствие/злость/усталость/воодушевление/нейтральное>",
  "emoji": "<один подходящий эмодзи>",
  "summary": "<1-2 предложения: что произошло или что чувствует человек>",
  "insight": "<1-2 предложения: психологическое наблюдение или мягкий совет>",
  "question": "<один открытый вопрос, чтобы помочь человеку глубже осмыслить ситуацию>"
}"""

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


async def analyze_entry(text: str) -> dict:
    last_error = ""

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=MODEL,
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                )
            )
            raw = response.text.strip()

            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            return json.loads(raw)

        except json.JSONDecodeError:
            return _fallback("Не удалось разобрать ответ AI.")

        except Exception as e:
            last_error = str(e)
            is_rate_limit = "429" in last_error or "quota" in last_error.lower()

            if is_rate_limit and attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY * attempt)
                continue

            break

    return _fallback(last_error)


def _fallback(reason: str) -> dict:
    return {
        "mood": "нейтральное",
        "emoji": "📝",
        "summary": "Запись сохранена.",
        "insight": f"Анализ временно недоступен: {reason}",
        "question": "Как ты себя чувствуешь прямо сейчас?",
    }


def format_analysis(analysis: dict) -> str:
    return (
        f"{analysis['emoji']} <b>Настроение:</b> {analysis['mood']}\n\n"
        f"<b>Краткое резюме:</b>\n{analysis['summary']}\n\n"
        f"<b>Наблюдение:</b>\n{analysis['insight']}\n\n"
        f"💭 <i>{analysis['question']}</i>"
    )