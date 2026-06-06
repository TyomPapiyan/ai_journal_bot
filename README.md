# 📔 AI Daily Journal Bot

An AI-powered Telegram bot for personal journaling with mood analysis. Write about your day — receive a warm, psychologically-aware response, a meaningful insight, and a reflective follow-up question.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Gemini](https://img.shields.io/badge/Gemini-2.5--flash-orange?logo=google)
![aiogram](https://img.shields.io/badge/aiogram-3-blue)

---

## ✨ Features

- **✍️ New Entry** — write freely about your day, thoughts, or feelings
- **📖 My Entries** — browse your last 10 journal entries at any time
- **📊 Statistics** — visualize your mood distribution and track emotional patterns over time
- **🤖 AI Analysis** — Gemini AI detects your mood, summarizes the entry, provides a psychological insight, and asks a thoughtful follow-up question
- **💬 Dialog Mode** — continue the conversation with the AI after each journal entry for deeper reflection

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core language |
| [aiogram 3](https://github.com/aiogram/aiogram) | Telegram bot framework |
| [Google Gemini API](https://ai.google.dev) (gemini-2.5-flash) | AI mood analysis and response generation |
| SQLite | Local persistent storage for journal entries |
| python-dotenv | Environment variable management |

---

## 📁 Project Structure

```
ai_journal_bot/
├── .env                  # Secret keys (not tracked by Git)
├── .gitignore
├── main.py               # Application entry point
├── bot/
│   ├── __init__.py
│   ├── handlers.py       # All Telegram bot handlers
│   └── keyboards.py      # Reply and inline keyboards
├── ai/
│   ├── __init__.py
│   └── analyzer.py       # Google Gemini API integration
└── database/
    ├── __init__.py
    └── db.py             # SQLite database logic
```

> ⚠️ `.env` and `journal.db` are excluded from version control via `.gitignore` — your API keys and personal diary entries remain private.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/TyomPapiyan/ai_journal_bot.git
cd ai_journal_bot
```

### 2. Create a virtual environment

```bash
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
```

### 3. Install dependencies

```bash
pip install aiogram python-dotenv google-generativeai google-genai
```

> The full list from the original setup (including optional libraries for potential future features):
> ```bash
> pip install aiogram python-dotenv anthropic openai pandas matplotlib opencv-python Pillow google-generativeai google-genai
> ```

### 4. Create the `.env` file

Create a file named `.env` in the project root with the following content:

```env
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

- **BOT_TOKEN** — obtain from [@BotFather](https://t.me/BotFather) on Telegram
- **GEMINI_API_KEY** — get a free key at [aistudio.google.com](https://aistudio.google.com)

### 5. Run the bot

```bash
python main.py
```

---

## 💬 Example Interaction

```
You:  Today was tough. I had a big presentation at work and I was very nervous.

Bot:  😰 Mood: Anxiety

      Summary:
      You experienced significant stress due to an important work presentation.

      Insight:
      Nervousness before important events is natural — it shows you care about the result.

      💭 What would have made you feel more confident going into it?
```

---

## 📋 Bot Commands

| Command | Description |
|---|---|
| `/start` | Start the bot and open the main menu |
| `/restart` | Reset the current session |
| `/end` | End the current session |
| `/help` | Show available commands and usage tips |

---

## 🗄 Database

The bot stores journal entries locally in a SQLite database (`journal.db`), which is created automatically on first run. Each entry includes the user's Telegram ID, the entry text, the detected mood, and a timestamp. The file is listed in `.gitignore` and never committed to the repository.

---

## 🔐 Privacy

- All data is stored locally on the machine running the bot.
- No journal entries or personal data are sent to any third party other than the Google Gemini API for analysis.
- Your `.env` file (containing API keys) and `journal.db` (containing diary entries) are excluded from Git by default.

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

```
MIT License — © 2026 TyomPapiyan
```

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome. Feel free to open an issue or submit a pull request on [GitHub](https://github.com/TyomPapiyan/ai_journal_bot).