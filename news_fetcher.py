"""
News Fetcher Module
───────────────────
Fetches the latest top headlines about Ethiopia from RSS feeds.
Uses Google News RSS by default, which aggregates from all major
sources (Reuters, BBC, Al Jazeera, etc.) — no API key required.
"""

import html
import logging
import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from email.utils import parsedate_to_datetime

import feedparser

import config

logger = logging.getLogger(__name__)


def fetch_ethiopia_news(max_articles: int | None = None) -> list[dict]:
    """
    Fetch the top Ethiopia news articles from configured RSS feeds.

    Returns a list of dicts, each containing:
        - title       (str)
        - description (str)
        - url         (str)
        - source      (str)
        - published_at (str)  – human-readable date string

    Returns an empty list on failure.
    """
    count = max_articles or config.RSS_MAX_ARTICLES
    all_articles = []

    for feed_url in config.RSS_FEEDS:
        try:
            logger.info("📡 Fetching RSS feed: %s", feed_url[:80])
            feed = feedparser.parse(feed_url)

            if feed.bozo and not feed.entries:
                logger.warning("⚠️  Feed error: %s", feed.bozo_exception)
                continue

            for entry in feed.entries:
                # Parse publication date
                published_nice = ""
                if hasattr(entry, "published"):
                    try:
                        dt = parsedate_to_datetime(entry.published)
                        published_nice = dt.strftime("%b %d, %Y • %H:%M UTC")
                    except Exception:
                        published_nice = entry.published
                elif hasattr(entry, "updated"):
                    published_nice = entry.updated

                # Extract source name
                source = _extract_source(entry)

                # Get the longest available description text
                raw_desc = _get_longest_text(entry)
                description = _strip_html(raw_desc)

                all_articles.append({
                    "title":        entry.get("title", "Untitled"),
                    "description":  description,
                    "url":          entry.get("link", ""),
                    "source":       source,
                    "published_at": published_nice,
                })

        except Exception as exc:
            logger.error("💥 Error fetching feed %s: %s", feed_url[:60], exc)

    if not all_articles:
        logger.warning("⚠️  No articles found across all feeds.")
        return []

    # Fuzzy deduplicate — catches near-duplicate headlines across sources
    unique = _deduplicate(all_articles)

    # Trim to max count
    result = unique[:count]
    logger.info("✅ Fetched %d articles successfully.", len(result))
    return result


def _extract_source(entry) -> str:
    """Try to pull the source name from the RSS entry."""
    # Google News includes source in the entry
    if hasattr(entry, "source"):
        return entry.source.get("title", "Unknown")
    # Some feeds put it in dc:creator or author
    if hasattr(entry, "author") and entry.author:
        return entry.author
    # Fall back to extracting from title (Google News format: "Title - Source")
    title = entry.get("title", "")
    if " - " in title:
        return title.rsplit(" - ", 1)[-1].strip()
    return "Unknown"


def _get_longest_text(entry) -> str:
    """
    Pull the longest available text from the RSS entry.

    feedparser entries can have: content[0].value, summary, description.
    We pick the longest one to maximise description richness.
    """
    candidates = []

    # content field (often the richest)
    if hasattr(entry, "content") and entry.content:
        for c in entry.content:
            val = c.get("value", "")
            if val:
                candidates.append(val)

    # summary field
    if entry.get("summary"):
        candidates.append(entry["summary"])

    # description field
    if entry.get("description"):
        candidates.append(entry["description"])

    if not candidates:
        return ""

    # Return the longest
    return max(candidates, key=len)

# ── Lightweight NLP deduplication ────────────────────────────────────────────
_STOPWORDS = frozenset(
    "a an the in on at to for of and or but is are was were be been "
    "by from with that this it its as has have had will can may".split()
)


def _normalize(text: str) -> str:
    """Lowercase, strip punctuation & stopwords for fuzzy comparison."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)          # remove punctuation
    words = [w for w in text.split() if w not in _STOPWORDS]
    return " ".join(words)


def _deduplicate(articles: list[dict], threshold: float = 0.65) -> list[dict]:
    """
    Remove near-duplicate articles using fuzzy title similarity.

    Uses difflib.SequenceMatcher on normalized titles:
      - Strips punctuation, lowercases, removes stopwords
      - Compares every pair; keeps the first occurrence
      - threshold=0.65 catches rephrasings while avoiding false positives
    """
    kept: list[dict] = []
    kept_normalized: list[str] = []

    for article in articles:
        norm = _normalize(article["title"])
        is_dup = False
        for seen in kept_normalized:
            if SequenceMatcher(None, norm, seen).ratio() >= threshold:
                is_dup = True
                break
        if not is_dup:
            kept.append(article)
            kept_normalized.append(norm)

    removed = len(articles) - len(kept)
    if removed:
        logger.info("🧹 Removed %d near-duplicate article(s).", removed)
    return kept


def _strip_html(text: str) -> str:
    """Remove HTML tags and decode all HTML entities."""
    clean = re.sub(r"<[^>]+>", "", text)
    clean = html.unescape(clean)     # &#8230; → …, &amp; → &, etc.
    return clean.strip()


# ── Quick test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    articles = fetch_ethiopia_news()
    for i, a in enumerate(articles, 1):
        print(f"\n{'─'*50}")
        print(f"  {i}. {a['title']}")
        print(f"     {a['source']} — {a['published_at']}")
        print(f"     {a['url']}")
