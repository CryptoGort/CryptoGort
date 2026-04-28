import xml.etree.ElementTree as ET

import requests
import yfinance as yf

STOCK_TICKERS = {
    "^GSPC": "S&P 500",
    "^IXIC": "NASDAQ",
    "^DJI": "Dow Jones",
}

CRYPTO_IDS = ["bitcoin", "ethereum", "solana"]

NEWS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
]

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,ethereum,solana"
    "&vs_currencies=usd"
    "&include_24hr_change=true"
)

COINGECKO_NAMES = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum",
    "solana": "Solana",
}


def _fetch_crypto_coingecko() -> dict:
    resp = requests.get(COINGECKO_URL, timeout=10)
    resp.raise_for_status()
    result = {}
    for coin_id, values in resp.json().items():
        name = COINGECKO_NAMES.get(coin_id, coin_id)
        result[name] = {
            "price": values["usd"],
            "change_pct": values.get("usd_24h_change", 0.0),
        }
    return result


def _fetch_crypto_yfinance() -> dict:
    data = {}
    for ticker, name in {"BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "SOL-USD": "Solana"}.items():
        try:
            hist = yf.Ticker(ticker).history(period="2d")
            if len(hist) >= 2:
                prev = hist["Close"].iloc[-2]
                current = hist["Close"].iloc[-1]
                data[name] = {"price": current, "change_pct": ((current - prev) / prev) * 100}
            elif len(hist) == 1:
                data[name] = {"price": hist["Close"].iloc[-1], "change_pct": 0.0}
        except Exception:
            pass
    return data


def get_market_data() -> dict:
    data = {}

    # Stock indices via yfinance
    for ticker, name in STOCK_TICKERS.items():
        try:
            hist = yf.Ticker(ticker).history(period="2d")
            if len(hist) >= 2:
                prev = hist["Close"].iloc[-2]
                current = hist["Close"].iloc[-1]
                data[name] = {"price": current, "change_pct": ((current - prev) / prev) * 100}
            elif len(hist) == 1:
                data[name] = {"price": hist["Close"].iloc[-1], "change_pct": 0.0}
        except Exception as e:
            print(f"Warning: could not fetch {ticker}: {e}")

    # Crypto — CoinGecko first, yfinance fallback
    try:
        data.update(_fetch_crypto_coingecko())
    except Exception as e:
        print(f"Warning: CoinGecko failed ({e}), trying yfinance...")
        data.update(_fetch_crypto_yfinance())

    return data


def get_crypto_news(max_items: int = 5) -> list[dict]:
    items = []
    headers = {"User-Agent": "CryptoGort-Bot/1.0"}
    for url in NEWS_FEEDS:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            # Atom feeds
            for entry in root.findall(".//atom:entry", ns)[:3]:
                title_el = entry.find("atom:title", ns)
                if title_el is not None and title_el.text:
                    items.append({"title": title_el.text.strip()})
            # RSS feeds
            for item in root.findall(".//item")[:3]:
                title_el = item.find("title")
                if title_el is not None and title_el.text:
                    items.append({"title": title_el.text.strip()})
            if len(items) >= max_items:
                return items[:max_items]
        except Exception as e:
            print(f"Warning: could not fetch feed {url}: {e}")
    return items[:max_items]


def format_market_summary(data: dict) -> str:
    lines = []
    for name, info in data.items():
        sign = "+" if info["change_pct"] >= 0 else ""
        lines.append(f"{name}: ${info['price']:,.2f} ({sign}{info['change_pct']:.2f}%)")
    return "\n".join(lines)
