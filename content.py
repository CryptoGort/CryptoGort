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
            "You are CryptoGort — a sharp, no-BS financial commentator on X. "
            "You cover stocks, crypto, macro, and world events with attitude. "
            "Your style is bold, provocative, and unapologetically opinionated — you call out "
            "market BS, name names, drop hot takes, and stir up debate to drive engagement. "
            "Think financial Twitter meets late-night radio host. You're not rude or offensive, "
            "but you're edgy, irreverent, and always say what others are thinking but won't say. "
            "You occasionally drop strategy gems that make followers feel like insiders. "
            "Always stay under 280 characters. Never wrap the tweet in quotes."
        ),
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def generate_premarket_post(market_data: dict, news: list[dict]) -> str:
    market_str = format_market_summary(market_data) if market_data else "(data unavailable)"
    headlines = "\n".join(f"• {n['title']}" for n in news[:5]) if news else "(no headlines available)"

    prompt = (
        "Write a pre-market tweet for 8:00 AM ET. Be loud and opinionated — tell people exactly "
        "what's about to happen and why Wall Street doesn't want them to know. "
        "Call out a key level to watch, drop a spicy take on a news headline, and end with "
        "a question or call-to-action that makes followers feel like they'd be idiots to ignore it. "
        "2-3 punchy hashtags.\n\n"
        f"Market data:\n{market_str}\n\n"
        f"Headlines:\n{headlines}"
    )
    return _ask_claude(prompt)


def generate_midday_post(market_data: dict, news: list[dict]) -> str:
    market_str = format_market_summary(market_data) if market_data else "(data unavailable)"
    headlines = "\n".join(f"• {n['title']}" for n in news[:4]) if news else "(no headlines available)"

    prompt = (
        "Write a midday market tweet for 12:00 PM ET. Mix humor with a real market insight — "
        "could be a meme-style observation, a savage hot take on something happening in the market "
        "right now, or a strategy tip disguised as a joke. Make it shareable and controversial enough "
        "that people want to reply. 1-2 hashtags.\n\n"
        f"Current market snapshot:\n{market_str}\n\n"
        f"What's happening:\n{headlines}"
    )
    return _ask_claude(prompt, max_tokens=200)


def generate_recap_post(market_data: dict, news: list[dict]) -> str:
    market_str = format_market_summary(market_data) if market_data else "(data unavailable)"
    headlines = "\n".join(f"• {n['title']}" for n in news[:5]) if news else "(no headlines available)"

    prompt = (
        "Write a market close recap tweet for 4:15 PM ET. Be brutally honest about what happened "
        "today — who got wrecked, who called it right, what the numbers actually mean. "
        "Drop a forward-looking strategy take for tomorrow or the week ahead. "
        "Make followers feel like they just got a briefing most people pay thousands for. "
        "End with something that makes them want to come back tomorrow. 2-3 hashtags.\n\n"
        f"Closing market data:\n{market_str}\n\n"
        f"Today's big stories:\n{headlines}"
    )
    return _ask_claude(prompt)
