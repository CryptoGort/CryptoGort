"""
CryptoGort X Automation
Scheduled posts (all times Eastern):
  08:30 - Pre-market commentary
  12:00 - Midday meme
  16:05 - Market recap
"""

import os
import logging
from datetime import datetime

import pytz
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv()

from market_data import get_market_data, get_crypto_news
from content import generate_premarket_post, generate_meme_post, generate_recap_post
from poster import post_tweet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

ET = pytz.timezone("America/New_York")


def job_premarket():
    log.info("Running pre-market post...")
    try:
        market_data = get_market_data()
        news = get_crypto_news()
        tweet = generate_premarket_post(market_data, news)
        log.info("Tweet:\n%s", tweet)
        post_tweet(tweet)
        log.info("Pre-market post complete.")
    except Exception:
        log.exception("Pre-market post failed")


def job_meme():
    log.info("Running noon meme post...")
    try:
        tweet = generate_meme_post()
        log.info("Tweet:\n%s", tweet)
        post_tweet(tweet)
        log.info("Meme post complete.")
    except Exception:
        log.exception("Meme post failed")


def job_recap():
    log.info("Running market recap post...")
    try:
        market_data = get_market_data()
        news = get_crypto_news()
        tweet = generate_recap_post(market_data, news)
        log.info("Tweet:\n%s", tweet)
        post_tweet(tweet)
        log.info("Recap post complete.")
    except Exception:
        log.exception("Recap post failed")


def main():
    scheduler = BlockingScheduler(timezone=ET)

    scheduler.add_job(job_premarket, "cron", hour=8, minute=30, id="premarket")
    scheduler.add_job(job_meme, "cron", hour=12, minute=0, id="meme")
    scheduler.add_job(job_recap, "cron", hour=16, minute=5, id="recap")

    log.info("CryptoGort scheduler started. Posts at 8:30 AM, 12:00 PM, 4:05 PM ET.")
    log.info("Next scheduled runs:")
    for job in scheduler.get_jobs():
        log.info("  %s → %s", job.id, job.next_run_time)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
