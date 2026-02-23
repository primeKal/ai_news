"""
Centralized configuration loader.
Loads environment variables from .env and exposes them as module-level constants.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ── RSS Feeds ────────────────────────────────────────────────────────────────
# RSS feeds — no API key required! Add or remove feeds as you like.
RSS_FEEDS = [
    # ── Local Ethiopian Sources ──────────────────────────────────────────
    "https://addisstandard.com/feed/",                              # Addis Standard
    "https://www.thereporterethiopia.com/feed/",                    # Ethiopian Reporter
    "https://www.ena.et/web/eng/rss",                               # Ethiopian News Agency (ENA)
    # ── International Sources ────────────────────────────────────────────
    "https://news.google.com/rss/search?q=Ethiopia&hl=en-US&gl=US&ceid=US:en",  # Google News
    "https://www.aljazeera.com/xml/rss/all.xml",                    # Al Jazeera
]
RSS_MAX_ARTICLES = 6    # Max articles to include in each message

# ── Telegram ─────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

# ── Scheduler ────────────────────────────────────────────────────────────────
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "8"))
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", "0"))


def validate_config():
    """Ensure all required environment variables are set."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHANNEL_ID:
        missing.append("TELEGRAM_CHANNEL_ID")

    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        print("   Copy .env.example to .env and fill in your keys.")
        sys.exit(1)
