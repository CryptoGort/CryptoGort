"""
CryptoGort X Automation
Scheduled posts (all times Eastern):
  08:00 - Pre-market commentary
  12:00 - Midday market + meme post
  16:15 - Market recap + strategy
"""

import logging

import pytz
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv()

from market_data import get_market_data, get_news
from content import generate_premarket_post, generate_midday_post, generate_recap_post
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
        news = get_news()
        tweet = generate_premarket_post(market_data, news)
        log.info("Tweet:\n%s", tweet)
        post_tweet(tweet)
        log.info("Pre-market post complete.")
    except Exception:
        log.exception("Pre-market post failed")


def job_midday():
    log.info("Running midday post...")
    try:
        market_data = get_market_data()
        news = get_news()
        tweet = generate_midday_post(market_data, news)
        log.info("Tweet:\n%s", tweet)
        post_tweet(tweet)
        log.info("Midday post complete.")
    except Exception:
        log.exception("Midday post failed")


def job_recap():
    log.info("Running market recap post...")
    try:
        market_data = get_market_data()
        news = get_news()
        tweet = generate_recap_post(market_data, news)
        log.info("Tweet:\n%s", tweet)
        post_tweet(tweet)
        log.info("Recap post complete.")
    except Exception:
        log.exception("Recap post failed")


def main():
    scheduler = BlockingScheduler(timezone=ET)

    scheduler.add_job(job_premarket, "cron", hour=8,  minute=0,  id="premarket")
    scheduler.add_job(job_midday,    "cron", hour=12, minute=0,  id="midday")
    scheduler.add_job(job_recap,     "cron", hour=16, minute=15, id="recap")

    log.info("CryptoGort scheduler started. Posts at 8:00 AM, 12:00 PM, 4:15 PM ET.")
    for job in scheduler.get_jobs():
        log.info("  %s → next run %s", job.id, job.next_run_time)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
