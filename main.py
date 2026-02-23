"""
Ethiopia Daily News Bot — Main Entry Point
───────────────────────────────────────────
Orchestrates:  fetch news → format message → send to Telegram

Usage
─────
  python main.py               Run once (great for cron / Railway scheduled jobs)
  python main.py --schedule    Run on a recurring daily schedule (local mode)
"""

import argparse
import logging

from apscheduler.schedulers.blocking import BlockingScheduler

import config
from news_fetcher import fetch_ethiopia_news
from message_formatter import format_news_message
from telegram_sender import send_message

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
    parser = argparse.ArgumentParser(description="Ethiopia Daily News Telegram Bot")
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run on a recurring daily schedule instead of a single execution.",
    )
    args = parser.parse_args()

    # Validate env vars
    config.validate_config()

    if args.schedule:
        logger.info(
            "🕑 Scheduling daily job at %02d:%02d UTC …",
            config.SCHEDULE_HOUR,
            config.SCHEDULE_MINUTE,
        )

        scheduler = BlockingScheduler()
        scheduler.add_job(
            run_daily_job,
            trigger="cron",
            hour=config.SCHEDULE_HOUR,
            minute=config.SCHEDULE_MINUTE,
        )

        # Also run immediately on startup
        run_daily_job()

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("👋 Scheduler stopped. Goodbye!")
    else:
        # Single run mode — ideal for cron jobs & Railway scheduled tasks
        run_daily_job()


if __name__ == "__main__":
    main()
