import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def daily_sync_job():
    """Run the daily card sync task."""
    from .card_fetcher import sync_upcoming_events
    from predictions.predictor import generate_prediction
    from events.models import Fight

    logger.info("Starting daily sync job...")

    events = sync_upcoming_events()

    for event in events:
        for fight in event.fights.filter(prediction__isnull=True):
            try:
                generate_prediction(fight)
                logger.info(f"Generated prediction for {fight}")
            except Exception as e:
                logger.error(f"Failed to generate prediction for {fight}: {e}")

    logger.info("Daily sync job completed.")


def start():
    """Initialize and start the scheduler. Only runs once."""
    if os.environ.get("RUN_MAIN") != "true":
        return

    if scheduler.running:
        return

    scheduler.add_job(
        daily_sync_job,
        trigger=IntervalTrigger(hours=24),
        id="daily_card_sync",
        name="Daily UFC Card Sync",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started — daily sync job registered.")
