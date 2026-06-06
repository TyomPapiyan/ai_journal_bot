# 📔 AI Daily Journal Bot

An AI-powered Telegram bot for personal journaling with mood analysis. Write about your day — receive a warm, psychologically-aware response, a meaningful insight, and a reflective follow-up question.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Gemini](https://img.shields.io/badge/Gemini-2.5--flash-orange?logo=google)
![aiogram](https://img.shields.io/badge/aiogram-3-blue)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws)

---

## ✨ Features

- **✍️ New Entry** — write freely about your day, thoughts, or feelings
- **📖 My Entries** — browse your last 10 journal entries at any time
- **📊 Statistics** — visualize your mood distribution and track emotional patterns over time
- **🤖 AI Analysis** — Gemini AI detects your mood, summarizes the entry, provides a psychological insight, and asks a thoughtful follow-up question
- **💬 Dialog Mode** — continue the conversation with the AI after each journal entry for deeper reflection
- **🌍 Multilingual Support** — the bot works in **English**, **Russian**, and **Armenian** (EN / RU / HY)

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core language |
| [aiogram 3](https://github.com/aiogram/aiogram) | Telegram bot framework |
| [Google Gemini API](https://ai.google.dev) (gemini-2.5-flash) | AI mood analysis and response generation |
| SQLite | Local persistent storage for journal entries |
| python-dotenv | Environment variable management |
| Docker | Containerized deployment |
| AWS EC2 | Cloud server hosting |

---

## 📁 Project Structure

```
ai_journal_bot/
├── .env                  # Secret keys (not tracked by Git)
├── .gitignore
├── main.py               # Application entry point
├── Dockerfile            # Docker container configuration
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

## 🚀 Getting Started (Local)

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

### 4. Create the `.env` file

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

## 🐳 Docker Deployment

The bot has been tested and deployed using **Docker**. Containerization makes it easy to run on any machine or cloud server without worrying about environment setup.

### Dockerfile example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### Build and run with Docker

```bash
# Build the image
docker build -t ai_journal_bot .

# Run the container
docker run -d \
  --name journal_bot \
  --env-file .env \
  --restart unless-stopped \
  ai_journal_bot
```

### Useful Docker commands

```bash
# View running containers
docker ps

# View bot logs
docker logs -f journal_bot

# Stop the bot
docker stop journal_bot

# Restart the bot
docker restart journal_bot
```

---

## ☁️ AWS EC2 Deployment

The bot has been deployed and tested on an **AWS EC2** instance running Ubuntu. Below are the steps to replicate the setup.

### 1. Launch EC2 instance

- Go to AWS Console → EC2 → Launch Instance
- Choose **Ubuntu 22.04 LTS**
- Instance type: `t2.micro` (free tier) or higher
- Open port **22 (SSH)** in the security group

### 2. Connect and set up the server

```bash
# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

### 3. Deploy the bot

```bash
# Clone the repository
git clone https://github.com/TyomPapiyan/ai_journal_bot.git
cd ai_journal_bot

# Create .env file
nano .env
# Paste your BOT_TOKEN and GEMINI_API_KEY, then save

# Build and run with Docker
sudo docker build -t ai_journal_bot .
sudo docker run -d --name journal_bot --env-file .env --restart unless-stopped ai_journal_bot
```

### 4. Verify it's running

```bash
sudo docker ps
sudo docker logs -f journal_bot
```

The bot will now run 24/7 on the AWS server and automatically restart if it crashes.

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

## 🌍 Multilingual Support

The bot supports three languages and responds in the same language the user writes in:

| Language | Code |
|---|---|
| English | EN |
| Russian | RU |
| Armenian | HY |

---

## 🔐 Privacy

- All data is stored locally on the machine running the bot.
- No journal entries or personal data are sent to any third party other than the Google Gemini API for analysis.
- Your `.env` file and `journal.db` are excluded from Git by default.

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

```
MIT License — © 2026 TyomPapiyan
```

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome. Feel free to open an issue or submit a pull request on [GitHub](https://github.com/TyomPapiyan/ai_journal_bot).