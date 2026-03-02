"""
Ethiopia Daily News Bot — Main Entry Point
───────────────────────────────────────────
Orchestrates:  fetch news → format message → send to Telegram

Usage
─────
  python main.py               Run once (great for cron / Railway scheduled jobs)
  python main.py --schedule    Run on a recurring daily schedule (local mode)
"""

import logging

from src import config
from src.news_fetcher import fetch_ethiopia_news
from src.message_formatter import format_news_message
from src.telegram_sender import send_message

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Core job ─────────────────────────────────────────────────────────────────
def run_daily_job():
    """Fetch → Format → Send."""
    logger.info("🚀 Starting daily Ethiopia news job …")

    # 1. Fetch
    articles = fetch_ethiopia_news()
    logger.info("📰 %d article(s) fetched.", len(articles))

    # 2. Format
    message = format_news_message(articles)

    # 3. Send
    success = send_message(message)

    if success:
        logger.info("🎉 Daily news delivered successfully!")
    else:
        logger.error("❌ Failed to deliver daily news.")

    return success


# ── Entry point ──────────────────────────────────────────────────────────────
def main():
    # Validate env vars
    config.validate_config()

    # Single run mode — ideal for GitHub Actions or cron jobs
    run_daily_job()


if __name__ == "__main__":
    main()
