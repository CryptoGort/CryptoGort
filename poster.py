import os
import tweepy


def _get_client() -> tweepy.Client:
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
    )


def post_tweet(text: str) -> str:
    client = _get_client()
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    print(f"Posted tweet ID: {tweet_id}")
    return tweet_id
