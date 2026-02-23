# 🇪🇹 Ethiopia Daily News Telegram Bot

Automated bot that fetches the latest top news about **Ethiopia**, crafts a beautifully formatted message, and sends it to your **Telegram channel** — every single day.

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📰 **Smart News Fetching** | Top Ethiopia headlines via [GNews API](https://gnews.io/) |
| 🎨 **Beautiful Formatting** | Emoji-rich, HTML-styled Telegram messages |
| 📤 **Reliable Delivery** | Auto-retry with rate-limit handling |
| 🕐 **Daily Scheduling** | Built-in scheduler or external cron support |
| 🚀 **1-Click Deploy** | Railway-ready with `Procfile` + `railway.json` |

---

## 📁 Project Structure

```
ai_news/
├── config.py              # Centralized configuration
├── news_fetcher.py        # GNews API integration
├── message_formatter.py   # Beautiful HTML message builder
├── telegram_sender.py     # Telegram channel delivery
├── main.py                # Orchestrator + scheduler
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── Procfile               # Railway deployment
├── railway.json           # Railway cron config
└── README.md              # You are here!
```

---

## 🛠️ Setup

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd ai_news
pip install -r requirements.txt
```

### 2. Get API Keys

| Key | Where to get it |
|-----|-----------------|
| **GNews API Key** | [gnews.io](https://gnews.io/) → Sign up (free: 100 req/day) |
| **Telegram Bot Token** | Message [@BotFather](https://t.me/BotFather) → `/newbot` |
| **Channel ID** | Add bot as channel admin, then use [@get_id_bot](https://t.me/get_id_bot) |

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your actual keys:
```

```env
GNEWS_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHANNEL_ID=@your_channel_or_-100xxxxxxx
SCHEDULE_HOUR=8
SCHEDULE_MINUTE=0
```

### 4. Run

```bash
# Single run (send news now)
python main.py

# Continuous scheduling (runs daily at configured time)
python main.py --schedule
```

---

## 🚀 Deployment (Railway — Recommended)

[Railway](https://railway.app/) provides free-tier hosting with built-in cron jobs.

### Steps

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app/) → **New Project** → **Deploy from GitHub**
3. Add environment variables in the Railway dashboard:
   - `GNEWS_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHANNEL_ID`
4. Railway will auto-detect the `Procfile` and `railway.json`
5. The bot will run daily at **8:00 AM UTC** automatically via the cron schedule

### Alternative: Linux Cron Job

```bash
# Open crontab
crontab -e

# Add this line to run daily at 8:00 AM UTC:
0 8 * * * cd /path/to/ai_news && /path/to/python main.py >> /var/log/ai_news.log 2>&1
```

---

## 📬 Sample Output

```
🇪🇹  ETHIOPIA DAILY NEWS  🇪🇹
📅  Monday, February 23, 2026

━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Ethiopia Signs Historic Peace Agreement

    📝  A landmark peace deal was signed today …

    🗞  Reuters  •  🕐  Feb 23, 2026 • 10:00 UTC

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

2️⃣  Addis Ababa Tech Hub Attracts Record Investment

    📝  International investors pour $500M …

    🗞  Bloomberg  •  🕐  Feb 23, 2026 • 08:30 UTC

━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖  Powered by AI News Bot
🔔  Stay informed — delivered daily!
```

---

## 🧩 Module Docs

| Module | Responsibility |
|--------|---------------|
| `config.py` | Loads `.env`, validates required keys |
| `news_fetcher.py` | Calls GNews API, parses articles |
| `message_formatter.py` | Builds emoji-rich HTML messages |
| `telegram_sender.py` | Sends to Telegram with retry logic |
| `main.py` | Wires everything + optional scheduler |

---

## 📄 License

MIT — use it however you like. If it's useful, give it a ⭐!
