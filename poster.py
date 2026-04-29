import os
import tweepy


def _check_credentials():
    keys = {
        "X_API_KEY": os.getenv("X_API_KEY"),
        "X_API_SECRET": os.getenv("X_API_SECRET"),
        "X_ACCESS_TOKEN": os.getenv("X_ACCESS_TOKEN"),
        "X_ACCESS_TOKEN_SECRET": os.getenv("X_ACCESS_TOKEN_SECRET"),
    }
    for name, val in keys.items():
        if not val:
            raise ValueError(f"Missing credential: {name}")
        print(f"  {name}: {val[:6]}...{val[-4:]} (len={len(val)})")


def _get_client() -> tweepy.Client:
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
    )


def verify_credentials():
    """Use v1.1 API to confirm keys are valid before attempting to post."""
    auth = tweepy.OAuth1UserHandler(
        os.getenv("X_API_KEY"),
        os.getenv("X_API_SECRET"),
        os.getenv("X_ACCESS_TOKEN"),
        os.getenv("X_ACCESS_TOKEN_SECRET"),
    )
    api = tweepy.API(auth)
    user = api.verify_credentials()
    print(f"Credentials verified. Authenticated as: @{user.screen_name}")
    return user


def post_tweet(text: str) -> str:
    print("Checking credentials...")
    _check_credentials()
    verify_credentials()
    client = _get_client()
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    print(f"Posted tweet ID: {tweet_id}")
    return tweet_id
