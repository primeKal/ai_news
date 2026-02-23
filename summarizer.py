"""
Summarizer Module
──────────────────
Handles AI-based summarization and rephrasing of news content.
Uses Google Gemini for generative rephrasing (to avoid copyright issues)
with a fallback to Sumy (extractive summarization).
"""

import logging
import json
import config

# Generative AI (Gemini)
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Extractive AI (Sumy)
try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lex_rank import LexRankSummarizer
    import nltk
    # Try to download punkt if not present
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
except ImportError:
    PlaintextParser = None

logger = logging.getLogger(__name__)

# Configure Gemini if key is provided
if genai and config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)
    # Using 'gemini-1.5-flash' directly. 
    # The 404 might be due to a version mismatch or transient issue.
    # We will try 'gemini-1.5-flash' as it's the standard.
    _model = genai.GenerativeModel('gemini-1.5-flash')
else:
    _model = None


def summarize_batch(articles: list[dict]) -> list[dict]:
    """
    Summarize a list of articles in a single AI call if possible.
    Updates the 'description' field of each article in-place.
    """
    if not articles:
        return articles

    mode = config.SUMMARIZATION_MODE.lower()

    if mode == "generative" and _model:
        return _summarize_batch_generative(articles)
    
    # Fallback to individual extractive summarization
    for article in articles:
        if PlaintextParser:
            article["description"] = _summarize_extractive(article["description"])
        else:
            article["description"] = article["description"][:800] + "..."
    
    return articles


def _summarize_batch_generative(articles: list[dict]) -> list[dict]:
    """Uses a single Gemini call to rephrase all articles."""
    logger.info("🤖 Summarizing %d articles in a single Gemini call...", len(articles))
    
    # Prepare the batch prompt
    items = []
    for i, a in enumerate(articles):
        items.append(f"ARTICLE {i+1}:\nTITLE: {a['title']}\nCONTENT: {a['description']}")
    
    batch_text = "\n\n".join(items)
    
    prompt = (
        "Rephrase the following news articles into 1-2 concise sentences each. "
        "Keep them neutral and informative. Do not use verbatim phrases from the source "
        "to ensure copyright safety. Focus on the core facts.\n"
        "Return the result as a JSON array of strings, where each string is the summary "
        "corresponding to the article order provided.\n\n"
        f"{batch_text}"
    )
    
    try:
        # Use generation_config to force JSON if possible, but keep it simple
        response = _model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        if response and response.text:
            summaries = json.loads(response.text)
            if isinstance(summaries, list) and len(summaries) == len(articles):
                for i, s in enumerate(summaries):
                    articles[i]["description"] = str(s).strip()
                return articles
            else:
                logger.warning("⚠️  Gemini returned unexpected JSON structure. Falling back.")
    except Exception as e:
        logger.error(f"Gemini batch summarization failed: {e}")
    
    # Final fallback: individual extractive
    for article in articles:
        article["description"] = _summarize_extractive(article["description"])
    
    return articles


def _summarize_extractive(text: str) -> str:
    """Uses Sumy to pick the most important sentences."""
    if not text or len(text) < 100 or not PlaintextParser:
        return text[:500] + "..."
        
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        sentences = summarizer(parser.document, config.MAX_SUMMARY_SENTENCES)
        
        summary = " ".join([str(s) for s in sentences])
        return summary if summary else text[:500] + "..."
    except Exception as e:
        logger.error(f"Extractive summarization failed: {e}")
        return text[:500] + "..."


if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.INFO)
    test_articles = [
        {
            "title": "Peace Deal Signed",
            "description": "Ethiopia has signed a landmark peace agreement that aims to end years of conflict. The deal was signed in Addis Ababa."
        },
        {
            "title": "Economic Growth",
            "description": "The Ethiopian economy is projected to grow by 7% this year despite global challenges, according to the latest report."
        }
    ]
    
    print("--- Batch Summarization ---")
    summarized = summarize_batch(test_articles)
    for a in summarized:
        print(f"\nTITLE: {a['title']}")
        print(f"SUMMARY: {a['description']}")
