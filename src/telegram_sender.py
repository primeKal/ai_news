"""
Telegram Sender Module
──────────────────────
Sends HTML-formatted messages to a Telegram channel via the Bot API.
"""

import asyncio
import logging

from telegram import Bot
from telegram.error import TelegramError, RetryAfter, TimedOut
from telegram.constants import ParseMode

import config

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


async def _send_async(text: str) -> bool:
    """
    Internal async sender with retry logic.

    Returns True on success, False on failure.
    """
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    channel = config.TELEGRAM_CHANNEL_ID

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("📤 Sending message to channel %s (attempt %d) …", channel, attempt)

            await bot.send_message(
                chat_id=channel,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )

            logger.info("✅ Message sent successfully!")
            return True

        except RetryAfter as exc:
            wait = exc.retry_after
            logger.warning("⏳ Rate limited — retrying after %d seconds …", wait)
            await asyncio.sleep(wait)

        except TimedOut:
            logger.warning("⏱️  Request timed out (attempt %d/%d).", attempt, MAX_RETRIES)
            await asyncio.sleep(2 * attempt)

        except TelegramError as exc:
            logger.error("🚫 Telegram API error: %s", exc)
            if attempt == MAX_RETRIES:
                return False
            await asyncio.sleep(2)

        except Exception as exc:
            logger.error("💥 Unexpected error: %s", exc)
            return False

    return False


def send_message(text: str) -> bool:
    """
    Send an HTML message to the configured Telegram channel.

    If the message exceeds Telegram's 4096 character limit,
    it is automatically split into multiple messages.

    Returns True if all parts were delivered, False otherwise.
    """
    MAX_LEN = 4096
    parts = _split_message(text, MAX_LEN) if len(text) > MAX_LEN else [text]

    if len(parts) > 1:
        logger.info("📐 Message is %d chars — splitting into %d parts.", len(text), len(parts))

    try:
        for part in parts:
            success = asyncio.run(_send_async(part))
            if not success:
                return False
        return True
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            for part in parts:
                success = loop.run_until_complete(_send_async(part))
                if not success:
                    return False
            return True
        finally:
            loop.close()


def _split_message(text: str, max_len: int) -> list[str]:
    """Split a long message on double-newlines, respecting max_len.
    Ensures HTML tags (<i>, <b>) are balanced in each part."""
    chunks = text.split("\n\n")
    parts = []
    current = ""

    for chunk in chunks:
        candidate = (current + "\n\n" + chunk) if current else chunk
        if len(candidate) <= max_len:
            current = candidate
        else:
            if current:
                parts.append(_close_open_tags(current))
            current = chunk[:max_len]

    if current:
        parts.append(_close_open_tags(current))

    return parts or [text[:max_len]]


def _close_open_tags(text: str) -> str:
    """Close any unclosed <i>, <b>, or <a> tags so Telegram doesn't reject it."""
    import re
    for tag in ("i", "b", "a"):
        open_count = len(re.findall(rf"<{tag}[ >]", text)) + text.count(f"<{tag}>")
        close_count = text.count(f"</{tag}>")
        # Deduplicate the <tag> and <tag > counts
        open_count = len(re.findall(rf"<{tag}(?:\s[^>]*)?>", text))
        if open_count > close_count:
            text += f"</{tag}>" * (open_count - close_count)
    return text


# ── Quick test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    config.validate_config()

    test_msg = (
        "🧪  <b>Test Message</b>\n\n"
        "If you see this, your Telegram bot is configured correctly! ✅"
    )
    success = send_message(test_msg)
    if success:
        print("\n🎉  Test message sent — check your channel!")
    else:
        print("\n❌  Failed to send test message. Check your config.")
