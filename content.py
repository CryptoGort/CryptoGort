import os
import anthropic
from market_data import format_market_summary

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client


def _ask_claude(prompt: str, max_tokens: int = 300) -> str:
    message = _get_client().messages.create(
        model="claude-opus-4-7",
        max_tokens=max_tokens,
        system=(
            "You are CryptoGort — a crypto enthusiast, blockchain advocate, and real estate "
            "tokenization pioneer on X. Your voice is confident, engaging, and community-focused. "
            "You write punchy tweets that educate and entertain your followers. "
            "Always stay under 280 characters. Never wrap the tweet in quotes."
        ),
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def generate_premarket_post(market_data: dict, news: list[dict]) -> str:
    market_str = format_market_summary(market_data) if market_data else "(data unavailable)"
    headlines = "\n".join(f"• {n['title']}" for n in news[:4]) if news else "(no headlines available)"

    prompt = (
        "Write a pre-market tweet (before 9:30 AM ET market open) that:\n"
        "- Highlights 1-2 key price levels or moves worth watching today\n"
        "- Weaves in a relevant news angle if fitting\n"
        "- Ends with an engaging hook or question for followers\n"
        "- Includes 2-3 hashtags (e.g. #Crypto #Bitcoin #Markets)\n\n"
        f"Live market data:\n{market_str}\n\n"
        f"Top headlines:\n{headlines}"
    )
    return _ask_claude(prompt)


def generate_meme_post() -> str:
    prompt = (
        "Write a funny, relatable crypto/trading meme tweet for 12:00 PM midday. "
        "Think: trader humor, HODLer mindset, or a witty observation about the market mood. "
        "Keep it light and shareable. 1-2 hashtags max."
    )
    return _ask_claude(prompt, max_tokens=150)


def generate_recap_post(market_data: dict, news: list[dict]) -> str:
    market_str = format_market_summary(market_data) if market_data else "(data unavailable)"
    headlines = "\n".join(f"• {n['title']}" for n in news[:4]) if news else "(no headlines available)"

    prompt = (
        "Write an end-of-day market recap tweet (markets just closed at 4 PM ET) that:\n"
        "- Summarizes the biggest move or story of the day in 1 sentence\n"
        "- Gives your take on what it means for crypto/blockchain\n"
        "- Closes with a forward-looking thought or question for tomorrow\n"
        "- Includes 2-3 hashtags\n\n"
        f"Final market data:\n{market_str}\n\n"
        f"Today's top stories:\n{headlines}"
    )
    return _ask_claude(prompt)
