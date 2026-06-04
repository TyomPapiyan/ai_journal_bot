# 📔 AI Daily Journal Bot

A Telegram bot for personal journaling with AI-powered mood analysis. Write about your day — get a warm psychological response, insight, and a reflective question.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Gemini](https://img.shields.io/badge/Gemini-2.5--flash-orange?logo=google)
![aiogram](https://img.shields.io/badge/aiogram-3-blue)

---

## ✨ Features

- ✍️ **New Entry** — write freely about your day or feelings
- 📖 **My Entries** — view your last 10 journal entries
- 📊 **Statistics** — track your mood distribution over time
- 🤖 **AI Analysis** — Gemini AI detects your mood, gives an insight and asks a follow-up question
- 💬 **Dialog mode** — continue the conversation with AI after each entry

---

## 🛠 Tech Stack

- Python 3.11
- [aiogram 3](https://github.com/aiogram/aiogram) — Telegram bot framework
- [Google Gemini API](https://ai.google.dev) — AI analysis (gemini-2.5-flash)
- SQLite — local database for entries
- python-dotenv

---

## 📁 Project Structure

```
ai_journal_bot/
├── .env                  # your secret keys (not in GitHub)
├── .gitignore
├── main.py               # entry point
├── bot/
│   ├── __init__.py
│   ├── handlers.py       # all bot handlers
│   └── keyboards.py      # reply & inline keyboards
├── ai/
│   ├── __init__.py
│   └── analyzer.py       # Gemini API integration
└── database/
    ├── __init__.py
    └── db.py             # SQLite logic
```

> ⚠️ `.env` and `journal.db` are excluded from GitHub via `.gitignore` — your keys and diary entries stay private.

---

## 🚀 Getting Started

**1. Clone the repository**

```
git clone https://github.com/TyomPapiyan/ai_journal_bot.git
cd ai_journal_bot
```

**2. Create virtual environment**

```
py -3.11 -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```
pip install aiogram python-dotenv anthropic openai pandas matplotlib opencv-python Pillow google-generativeai google-genai
```

**4. Create `.env` file**

```
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

- Get Telegram token from [@BotFather](https://t.me/BotFather)
- Get free Gemini API key from [aistudio.google.com](https://aistudio.google.com)

**5. Run the bot**

```
python main.py
```

---

## 💬 Example

```
You:  Today was tough. I had a big presentation at work and I was very nervous.

Bot:  😰 Mood: тревога

      Summary:
      You experienced significant stress due to an important work presentation.

      Insight:
      Nervousness before important events is natural — it shows you care about the result.

      💭 What would have made you feel more confident going into it?
```

---

## 📋 Commands

| Command     | Description           |
|-------------|-----------------------|
| `/start`    | Start the bot         |
| `/restart`  | Reset current session |
| `/end`      | End session           |
| `/help`     | Show help             |

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute it.

```
MIT License — © 2026 TyomPapiyan
```
