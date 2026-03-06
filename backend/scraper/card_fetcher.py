import logging
import time
from django.utils import timezone
from fighters.models import Fighter
from events.models import Event, Fight
from predictions.predictor import generate_prediction
from .ufcstats_scraper import scrape_events, scrape_event_fights, scrape_fighter

logger = logging.getLogger(__name__)

DELAY_BETWEEN_REQUESTS = 1.5  # be polite to ufcstats.com


def sync_upcoming_events():
    """Scrape upcoming + recent events from ufcstats.com and save to DB."""
    events_synced = []

    # Scrape upcoming events
    upcoming = scrape_events(page="completed", limit=3)
    logger.info(f"Found {len(upcoming)} events to sync")

    for event_data in upcoming:
        if not event_data["ufcstats_id"] or not event_data["date"]:
            continue

        event, created = Event.objects.update_or_create(
            sportradar_id=event_data["ufcstats_id"],
            defaults={
                "name": event_data["name"],
                "date": event_data["date"],
                "location": event_data["location"],
                "status": event_data["status"],
                "last_synced": timezone.now(),
            },
        )

        if event_data["url"]:
            time.sleep(DELAY_BETWEEN_REQUESTS)
            _sync_event_fights(event, event_data["url"])

        events_synced.append(event)

    # Also check upcoming page
    upcoming_events = scrape_events(page="upcoming", limit=3)
    for event_data in upcoming_events:
        if not event_data["ufcstats_id"] or not event_data["date"]:
            continue

        event, created = Event.objects.update_or_create(
            sportradar_id=event_data["ufcstats_id"],
            defaults={
                "name": event_data["name"],
                "date": event_data["date"],
                "location": event_data["location"],
                "status": "upcoming",
                "last_synced": timezone.now(),
            },
        )

        if event_data["url"]:
            time.sleep(DELAY_BETWEEN_REQUESTS)
            _sync_event_fights(event, event_data["url"])

        events_synced.append(event)

    logger.info(f"Synced {len(events_synced)} events total")
    return events_synced


def _sync_event_fights(event, event_url):
    """Scrape fights for an event and save to DB."""
    try:
        event_detail = scrape_event_fights(event_url)
    except Exception as e:
        logger.error(f"Failed to scrape fights for {event.name}: {e}")
        return

    for fight_data in event_detail["fights"]:
        fighter_a = _upsert_fighter(fight_data["fighter_a"])
        fighter_b = _upsert_fighter(fight_data["fighter_b"])

        if not fighter_a or not fighter_b:
            continue

        fight, created = Fight.objects.update_or_create(
            event=event,
            fighter_a=fighter_a,
            fighter_b=fighter_b,
            defaults={
                "weight_class": fight_data["weight_class"],
                "card_section": fight_data["card_section"],
                "order": fight_data["order"],
                "method": fight_data["method"],
            },
        )

        # Generate prediction if none exists
        if not hasattr(fight, "prediction") or fight.prediction is None:
            try:
                generate_prediction(fight)
                logger.info(f"Generated prediction for {fight}")
            except Exception as e:
                logger.warning(f"Could not generate prediction for {fight}: {e}")


def _upsert_fighter(fighter_data):
    """Create or update a fighter, scraping their full stats from ufcstats.com."""
    ufcstats_id = fighter_data.get("ufcstats_id", "")
    if not ufcstats_id:
        return None

    # Check if we already have this fighter with recent data (< 24h old)
    try:
        existing = Fighter.objects.get(sportradar_id=ufcstats_id)
        age = timezone.now() - existing.last_updated
        if age.total_seconds() < 86400:
            return existing
    except Fighter.DoesNotExist:
        pass

    # Scrape full fighter stats
    fighter_url = fighter_data.get("url", "")
    if not fighter_url:
        fighter_url = f"http://ufcstats.com/fighter-details/{ufcstats_id}"

    try:
        time.sleep(DELAY_BETWEEN_REQUESTS)
        stats = scrape_fighter(fighter_url)
    except Exception as e:
        logger.warning(f"Could not scrape fighter {fighter_data['name']}: {e}")
        # Create with minimal info
        fighter, _ = Fighter.objects.update_or_create(
            sportradar_id=ufcstats_id,
            defaults={"name": fighter_data["name"], "weight_class": ""},
        )
        return fighter

    fighter, _ = Fighter.objects.update_or_create(
        sportradar_id=ufcstats_id,
        defaults={
            "name": stats["name"] or fighter_data["name"],
            "nickname": stats["nickname"],
            "weight_class": stats["weight_class"],
            "record_wins": stats["record_wins"],
            "record_losses": stats["record_losses"],
            "record_draws": stats["record_draws"],
            "wins_ko_tko": stats["wins_ko_tko"],
            "wins_submission": stats["wins_submission"],
            "wins_decision": stats["wins_decision"],
            "losses_ko_tko": stats["losses_ko_tko"],
            "losses_submission": stats["losses_submission"],
            "losses_decision": stats["losses_decision"],
            "sig_strikes_per_min": stats["sig_strikes_per_min"],
            "strike_accuracy": stats["strike_accuracy"],
            "takedown_avg": stats["takedown_avg"],
            "takedown_accuracy": stats["takedown_accuracy"],
            "takedown_defense": stats["takedown_defense"],
            "sub_attempts_per_min": stats["sub_attempts_per_min"],
        },
    )
    return fighter
