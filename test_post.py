"""
Run a specific post type manually to verify the full pipeline.
Usage:
  python test_post.py premarket
  python test_post.py meme
  python test_post.py recap
  python test_post.py all          # dry-run all three (no posting)
  python test_post.py premarket --post  # actually post to X
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

from market_data import get_market_data, get_crypto_news
from content import generate_premarket_post, generate_meme_post, generate_recap_post
from poster import post_tweet


def run(post_type: str, do_post: bool):
    market_data = get_market_data() if post_type != "meme" else {}
    news = get_crypto_news() if post_type != "meme" else []

    if post_type == "premarket":
        tweet = generate_premarket_post(market_data, news)
    elif post_type == "meme":
        tweet = generate_meme_post()
    elif post_type == "recap":
        tweet = generate_recap_post(market_data, news)
    else:
        print(f"Unknown type: {post_type}")
        sys.exit(1)

    print(f"\n--- {post_type.upper()} TWEET ({len(tweet)} chars) ---")
    print(tweet)
    print("---\n")

    if do_post:
        tweet_id = post_tweet(tweet)
        print(f"Posted! Tweet ID: {tweet_id}")
    else:
        print("Dry run — use --post flag to actually post.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    post_type = args[0]
    do_post = "--post" in args

    if post_type == "all":
        market_data = get_market_data()
        news = get_crypto_news()
        for t, fn in [
            ("premarket", lambda: generate_premarket_post(market_data, news)),
            ("meme", generate_meme_post),
            ("recap", lambda: generate_recap_post(market_data, news)),
        ]:
            tweet = fn()
            print(f"\n--- {t.upper()} ({len(tweet)} chars) ---")
            print(tweet)
        print("\nDry run complete.")
    else:
        run(post_type, do_post)
