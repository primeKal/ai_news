"""
Message Formatter Module
────────────────────────
Crafts a beautiful, emoji-rich HTML message for Telegram
from a list of news articles.
"""

from datetime import datetime, timezone


def format_news_message(articles: list[dict]) -> str:
    """
    Build a beautifully formatted Telegram HTML message.

    Parameters
    ----------
    articles : list[dict]
        Each dict should have: title, description, url, source, published_at.

    Returns
    -------
    str
        HTML string ready to send via Telegram (parse_mode=HTML).
    """
    if not articles:
        return _no_news_fallback()

    today = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")

    lines = []

    # ── Header ───────────────────────────────────────────────────────────
    lines.append("📰  <b>PAPI NEWS</b>")
    lines.append(f"<i>{today}</i>")
    lines.append("")
    lines.append("Your daily updates from the Horn 🌍")
    lines.append("Here are today's top curated news for you by Papi AI.")
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # ── Articles ─────────────────────────────────────────────────────────
    emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for idx, article in enumerate(articles):
        num_emoji = emoji_numbers[idx] if idx < len(emoji_numbers) else "▪️"

        title = _escape_html(article.get("title", "Untitled"))
        description = _escape_html(article.get("description", ""))
        url = article.get("url", "")
        source = _escape_html(article.get("source", "Unknown"))
        published = article.get("published_at", "")

        # Spacing before each article
        lines.append("")
        lines.append("")

        # Title with link
        lines.append(f'{num_emoji}  <a href="{url}">{title}</a>')

        # AI Generated Summary
        if description:
            lines.append(f"✨ <b>Quick Take (AI):</b>")
            lines.append(f"<i>{description}</i>")
        # Source & timestamp
        lines.append(f"🗞 {source}  ·  🕐 {published}")

        # Separator between articles
        if idx < len(articles) - 1:
            lines.append("")
            lines.append("  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─")

    # ── Footer ───────────────────────────────────────────────────────────
    lines.append("")
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("<i>Papi News · delivered daily</i>")

    return "\n".join(lines)


def _no_news_fallback() -> str:
    """Friendly message when no articles are available."""
    today = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")
    return (
        "📰  <b>PAPI NEWS</b>\n"
        f"<i>{today}</i>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "😴  No news articles found today.\n\n"
        "We'll try again tomorrow — stay tuned!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Papi News · delivered daily</i>"
    )


def _escape_html(text: str) -> str:
    """Escape characters that conflict with Telegram HTML parse mode."""
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ── Quick preview ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = [
        {
            "title": "Ethiopia Signs Historic Peace Agreement",
            "description": "A landmark peace deal was signed today in Addis Ababa, bringing hope for lasting stability in the region. Officials from both sides expressed optimism about the future.",
            "url": "https://example.com/peace",
            "source": "Reuters",
            "published_at": "Feb 23, 2026 • 10:00 UTC",
        },
        {
            "title": "Addis Ababa Tech Hub Attracts Record Investment",
            "description": "International investors pour $500M into Ethiopia's growing technology sector, marking a new milestone for the East African tech ecosystem.",
            "url": "https://example.com/tech",
            "source": "Bloomberg",
            "published_at": "Feb 23, 2026 • 08:30 UTC",
        },
    ]
    print(format_news_message(sample))
