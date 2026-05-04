import os
import anthropic
from market_data import format_market_summary

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client


def _ask_claude(prompt: str, max_tokens: int = 160) -> str:
    message = _get_client().messages.create(
        model="claude-opus-4-7",
        max_tokens=max_tokens,
        system=(
            "You are CryptoGort, a sharp no-BS financial commentator on X. "
            "Your focus is the broad market and major news events that move it. Stocks, indices, "
            "macro, geopolitics, fed, earnings, oil, gold, yields. Crypto only when it actually matters. "
            "Your style is bold, provocative, and unapologetically opinionated. You call out "
            "market BS, name names, drop hot takes, and stir up debate to drive engagement. "
            "Think financial Twitter meets late-night radio host. You are not rude or offensive "
            "but you are edgy, irreverent, and always say what others are thinking but won't say. "
            "You occasionally drop options strategy gems (IV crush, weekly chains, gamma flows, "
            "0DTE, put/call ratios, OPEX, premium selling, defined risk plays) that make followers "
            "feel like insiders. Mention specific tickers when relevant (SPY, QQQ, IWM, single names). "
            "Never use hyphens anywhere in the tweet. Write the way a real person talks, not like a list or a bot. "
            "End every tweet with exactly one relevant hashtag. No more, no less. "
            "Keep the body short enough that the closing hashtag always fits. Aim for under 240 characters total. "
            "Always stay under 280 characters. Never wrap the tweet in quotes."
        ),
        messages=[{"role": "user", "content": prompt}],
    )
    text = message.content[0].text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
    if len(text) > 280:
        text = _trim_clean(text, 280)
    return text


def _trim_clean(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    window = text[:limit]
    for punct in (". ", "! ", "? ", ".\n", "!\n", "?\n"):
        idx = window.rfind(punct)
        if idx >= limit - 80:
            return text[: idx + 1].rstrip()
    idx = window.rfind(" ")
    if idx > 0:
        return text[:idx].rstrip()
    return window.rstrip()


def generate_premarket_post(market_data: dict, news: list[dict]) -> str:
    market_str = format_market_summary(market_data) if market_data else "(data unavailable)"
    headlines = "\n".join(f"• {n['title']}" for n in news[:5]) if news else "(no headlines available)"

    prompt = (
        "Write a pre-market tweet for 8:00 AM ET. Lead with the broad market setup. "
        "Tie in one of the news headlines as the catalyst. Call out a key level on SPY, QQQ, "
        "or a specific ticker. Optionally mention an options angle if it fits naturally. "
        "End with a question or call to action that punches. "
        "No hyphens. Write it the way someone actually talks. Stay under 250 characters.\n\n"
        f"Market data:\n{market_str}\n\n"
        f"Headlines:\n{headlines}"
    )
    return _ask_claude(prompt)


def generate_midday_post(market_data: dict, news: list[dict]) -> str:
    market_str = format_market_summary(market_data) if market_data else "(data unavailable)"
    headlines = "\n".join(f"• {n['title']}" for n in news[:4]) if news else "(no headlines available)"

    prompt = (
        "Write a midday market tweet for 12:00 PM ET. Anchor it to what is actually happening "
        "in the tape or a news event today. Mix in humor or a savage hot take. "
        "Bonus if you sneak in an options observation without sounding like a textbook. "
        "Make it something people want to screenshot and share. "
        "No hyphens. Write it the way someone actually talks. Stay under 250 characters.\n\n"
        f"Current market snapshot:\n{market_str}\n\n"
        f"What's happening:\n{headlines}"
    )
    return _ask_claude(prompt)


def generate_recap_post(market_data: dict, news: list[dict]) -> str:
    market_str = format_market_summary(market_data) if market_data else "(data unavailable)"
    headlines = "\n".join(f"• {n['title']}" for n in news[:5]) if news else "(no headlines available)"

    prompt = (
        "Write a market close recap tweet for 4:15 PM ET. Be brutally honest about what happened today "
        "and tie the move to the news driver behind it. Say who got wrecked, who called it right. "
        "Drop a forward looking strategy take for tomorrow or the week ahead. "
        "End with something that makes them want to come back tomorrow. "
        "No hyphens. Write it the way someone actually talks. Stay under 250 characters.\n\n"
        f"Closing market data:\n{market_str}\n\n"
        f"Today's big stories:\n{headlines}"
    )
    return _ask_claude(prompt)
