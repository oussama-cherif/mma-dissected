import logging
from django.utils import timezone
from fighters.models import Fighter
from events.models import Event, Fight
from .sportradar_client import SportRadarClient

logger = logging.getLogger(__name__)


def sync_upcoming_events():
    """Fetch upcoming UFC events from SportRadar and update the database."""
    client = SportRadarClient()

    try:
        schedule_data = client.get_schedule()
    except Exception as e:
        logger.error(f"Failed to fetch schedule: {e}")
        return []

    events_synced = []
    sport_events = schedule_data.get("sport_events", [])

    for event_data in sport_events:
        event, _ = Event.objects.update_or_create(
            sportradar_id=event_data["id"],
            defaults={
                "name": event_data.get("name", "UFC Event"),
                "date": event_data.get("scheduled", timezone.now()),
                "location": event_data.get("venue", {}).get("city_name", ""),
                "venue": event_data.get("venue", {}).get("name", ""),
                "status": _map_status(event_data.get("status", "")),
                "last_synced": timezone.now(),
            },
        )
        events_synced.append(event)

        _sync_event_fights(client, event, event_data)

    logger.info(f"Synced {len(events_synced)} events")
    return events_synced


def _sync_event_fights(client, event, event_data):
    """Sync individual fights for an event."""
    competitions = event_data.get("sport_event_conditions", {}).get("competitors", [])

    for idx, fight_data in enumerate(event_data.get("competitions", [])):
        competitors = fight_data.get("competitors", [])
        if len(competitors) < 2:
            continue

        fighter_a = _upsert_fighter(client, competitors[0])
        fighter_b = _upsert_fighter(client, competitors[1])

        if fighter_a and fighter_b:
            Fight.objects.update_or_create(
                event=event,
                fighter_a=fighter_a,
                fighter_b=fighter_b,
                defaults={
                    "weight_class": fight_data.get("weight_class", "Unknown"),
                    "card_section": _map_card_section(fight_data.get("type", "")),
                    "order": idx,
                },
            )


def _upsert_fighter(client, competitor_data):
    """Create or update a fighter from SportRadar competitor data."""
    sr_id = competitor_data.get("id")
    if not sr_id:
        return None

    fighter_defaults = {
        "name": competitor_data.get("name", "Unknown Fighter"),
        "nationality": competitor_data.get("nationality", ""),
    }

    try:
        profile = client.get_fighter_profile(sr_id)
        stats = profile.get("statistics", {})
        fighter_defaults.update({
            "nickname": profile.get("nickname", ""),
            "weight_class": profile.get("weight_class", ""),
            "record_wins": stats.get("wins", 0),
            "record_losses": stats.get("losses", 0),
            "record_draws": stats.get("draws", 0),
            "wins_ko_tko": stats.get("wins_ko_tko", 0),
            "wins_submission": stats.get("wins_submission", 0),
            "wins_decision": stats.get("wins_decision", 0),
            "losses_ko_tko": stats.get("losses_ko_tko", 0),
            "losses_submission": stats.get("losses_submission", 0),
            "losses_decision": stats.get("losses_decision", 0),
            "sig_strikes_per_min": stats.get("sig_strikes_per_min"),
            "strike_accuracy": stats.get("strike_accuracy"),
            "takedown_avg": stats.get("takedown_avg"),
            "takedown_accuracy": stats.get("takedown_accuracy"),
            "takedown_defense": stats.get("takedown_defense"),
            "sub_attempts_per_min": stats.get("sub_attempts_per_min"),
        })
    except Exception as e:
        logger.warning(f"Could not fetch profile for fighter {sr_id}: {e}")

    fighter, _ = Fighter.objects.update_or_create(
        sportradar_id=sr_id,
        defaults=fighter_defaults,
    )
    return fighter


def _map_status(sr_status):
    """Map SportRadar event status to our internal status."""
    mapping = {
        "not_started": "upcoming",
        "live": "live",
        "closed": "completed",
        "ended": "completed",
    }
    return mapping.get(sr_status.lower(), "upcoming")


def _map_card_section(fight_type):
    """Map SportRadar fight type to card section."""
    fight_type_lower = fight_type.lower()
    if "main" in fight_type_lower:
        return "main"
    elif "prelim" in fight_type_lower and "early" in fight_type_lower:
        return "early"
    elif "prelim" in fight_type_lower:
        return "prelim"
    return "main"
