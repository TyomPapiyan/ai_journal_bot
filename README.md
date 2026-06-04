# 📔 AI Daily Journal Bot — @myjornalAI_bot

[![Python](https://camo.githubusercontent.com/cdb16a42e46d164ad70645c3f2c27c04da790e49dcc0b5395304734f4c723f00/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d332e31312d626c75653f6c6f676f3d707974686f6e)](https://python.org)
[![License](https://camo.githubusercontent.com/5caa455d8debc46fb23abbadb45a733a937f3910a73fc875c2f7820468e1bb54/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d677265656e)](LICENSE)
[![Gemini](https://camo.githubusercontent.com/149f3339db7177b984f39d0bfa80871c9fa43db7db62a3922b6d9eb3e36b501a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f47656d696e692d322e352d2d666c6173682d6f72616e67653f6c6f676f3d676f6f676c65)](https://ai.google.dev)
[![aiogram](https://camo.githubusercontent.com/7967eb79aba9d89b0482ce99c3550596839e90b69abb117c88980d614c28d591/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f61696f6772616d2d332d626c7565)](https://docs.aiogram.dev)

A Telegram bot for personal journaling with AI-powered mood analysis. Write about your day — get a warm psychological response, insight, and a reflective question.

Личный AI-дневник в Telegram с поддержкой трёх языков: 🇷🇺 Русский, 🇦🇲 Հայերեն, 🇬🇧 English.

🤖 Попробуй бота: t.me/myjornalAI_bot

---

## 🌍 Языки интерфейса / Languages

При первом запуске бот предлагает выбрать язык. Весь интерфейс, меню и ответы бота будут на выбранном языке:

| Язык / Language | Меню / Menu | Ответы / Responses |
|-----------------|-------------|-------------------|
| 🇷🇺 Русский | ✅ | ✅ |
| 🇦🇲 Հայերեն | ✅ | ✅ |
| 🇬🇧 English | ✅ | ✅ |

---

## ✨ Возможности / Features

- 📝 **Новая запись / New Entry** — напиши о своём дне, бот выслушает и даст тёплый AI-отклик с анализом настроения
- 💬 **Диалог / Dialog** — после записи можно продолжить разговор с ботом
- 📖 **Мои записи / My Entries** — просмотр последних 10 записей
- 📊 **Статистика / Statistics** — количество записей и распределение настроений
- 🌍 **Выбор языка / Language selection** — при старте и в любой момент

---

## 🤖 Технологии / Tech Stack

- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot framework
- [Google Gemini 2.5](https://ai.google.dev/) — анализ настроения и диалог / mood analysis & dialog
- SQLite — хранение записей и пользователей
- Docker — контейнеризация
- AWS EC2 — облачный сервер / cloud server

---

## ☁️ Деплой на AWS с Docker / Deploy on AWS with Docker

Бот разворачивается на **AWS EC2** сервере с помощью Docker — это позволяет запускать его стабильно 24/7.

### 1. Клонируй репозиторий на сервер

```bash
git clone https://github.com/TyomPapiyan/ai_journal_bot.git
cd ai_journal_bot
```

### 2. Собери Docker-образ

```bash
sudo docker build -t bot .
```

### 3. Запусти контейнер

```bash
sudo docker run -d \
  --name bot \
  --restart always \
  -e BOT_TOKEN="твой_telegram_токен" \
  -e GEMINI_API_KEY="твой_gemini_ключ" \
  bot
```

> `--restart always` — бот автоматически перезапускается после перезагрузки сервера

### 4. Полезные команды

```bash
sudo docker logs bot          # посмотреть логи
sudo docker stop bot          # остановить бота
sudo docker start bot         # запустить снова
sudo docker rm bot            # удалить контейнер
```

---

## 🔑 Переменные окружения / Environment Variables

| Переменная | Описание |
|------------|----------|
| `BOT_TOKEN` | Токен Telegram бота от [@BotFather](https://t.me/BotFather) |
| `GEMINI_API_KEY` | API ключ от [Google AI Studio](https://aistudio.google.com/app/apikey) |

---

## 📁 Структура проекта / Project Structure

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

---

## 💬 Команды бота / Bot Commands

| Команда | Описание |
|---------|----------|
| `/start` | Начать / выбрать язык / Start & choose language |
| `/restart` | Перезапустить бота / Restart bot |
| `/end` | Завершить сессию / End session |
| `/help` | Помощь / Help |

---

## 👨‍💻 Автор / Author

[@TyomPapiyan](https://github.com/TyomPapiyan)

---

## 📄 License

This project is licensed under the MIT License — feel free to use, modify, and distribute it.

MIT License — © 2026 TyomPapiyan
