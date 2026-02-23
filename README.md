# 🇪🇹 Ethiopia Daily News Telegram Bot

Automated bot that fetches the latest top news about **Ethiopia**, crafts a beautifully formatted message, and sends it to your **Telegram channel** — every single day.

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📰 **RSS Aggregation** | Multi-source feed parsing (Addis Standard, Reporter, ENA, etc.) |
| ✨ **AI Summaries** | Single-call Gemini batch rephrasing for copyright safety |
| 🎨 **Beautiful Formatting** | Emoji-rich, split-aware HTML delivery |
| 🚀 **Render Ready** | Blueprint for Render Cron Job included |

---

## 📁 Project Structure

```
ai_news/
├── config.py              # Feeds and AI settings
├── news_fetcher.py        # RSS engine + fuzzy deduplication
├── summarizer.py          # Gemini/Sumy AI logic
├── message_formatter.py   # Split-aware HTML builder
├── telegram_sender.py     # Tag-balancing delivery
├── main.py                # Main entry point
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── render.yaml            # Render Blueprint config
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
| **Telegram Bot Token** | Message [@BotFather](https://t.me/BotFather) → `/newbot` |
| **Gemini API Key** | [Google AI Studio](https://aistudio.google.com/) (Optional but recommended) |
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

## 🚀 Deployment (Render)

[Render](https://render.com/) is perfect for running this as a daily **Cron Job**.

### Steps

1. Push your code to GitHub.
2. Go to **Render Dashboard** → **Blueprints** → **New Blueprint**.
3. Connect your repository.
4. Render will detect `render.yaml` and set up the **Cron Job**.
5. Add your **Environment Variables** in the Render dashboard:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHANNEL_ID`
   - `GEMINI_API_KEY` (highly recommended)
6. The bot will run daily at **8:00 AM UTC**.

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
