"""
Seed script — populates the database with a sample UFC event and real fighter data.
Run with: python manage.py shell < seed_data.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from datetime import datetime, timezone
from fighters.models import Fighter
from events.models import Event, Fight

# --- Fighters (real stats, approximate) ---

fighters_data = [
    {
        "name": "Islam Makhachev",
        "nickname": "The Eagle's Successor",
        "weight_class": "Lightweight",
        "nationality": "Russia",
        "record_wins": 26,
        "record_losses": 1,
        "record_draws": 0,
        "wins_ko_tko": 5,
        "wins_submission": 12,
        "wins_decision": 9,
        "losses_ko_tko": 0,
        "losses_submission": 0,
        "losses_decision": 1,
        "sig_strikes_per_min": 4.07,
        "strike_accuracy": 59.0,
        "takedown_avg": 3.38,
        "takedown_accuracy": 60.0,
        "takedown_defense": 88.0,
        "sub_attempts_per_min": 1.2,
        "sportradar_id": "sr:competitor:makhachev",
    },
    {
        "name": "Alexander Volkanovski",
        "nickname": "The Great",
        "weight_class": "Featherweight",
        "nationality": "Australia",
        "record_wins": 26,
        "record_losses": 4,
        "record_draws": 0,
        "wins_ko_tko": 13,
        "wins_submission": 3,
        "wins_decision": 10,
        "losses_ko_tko": 1,
        "losses_submission": 1,
        "losses_decision": 2,
        "sig_strikes_per_min": 6.23,
        "strike_accuracy": 56.0,
        "takedown_avg": 1.82,
        "takedown_accuracy": 37.0,
        "takedown_defense": 71.0,
        "sub_attempts_per_min": 0.2,
        "sportradar_id": "sr:competitor:volkanovski",
    },
    {
        "name": "Jon Jones",
        "nickname": "Bones",
        "weight_class": "Heavyweight",
        "nationality": "United States",
        "record_wins": 27,
        "record_losses": 1,
        "record_draws": 0,
        "wins_ko_tko": 10,
        "wins_submission": 7,
        "wins_decision": 10,
        "losses_ko_tko": 0,
        "losses_submission": 0,
        "losses_decision": 1,
        "sig_strikes_per_min": 4.35,
        "strike_accuracy": 57.0,
        "takedown_avg": 1.87,
        "takedown_accuracy": 44.0,
        "takedown_defense": 95.0,
        "sub_attempts_per_min": 0.5,
        "sportradar_id": "sr:competitor:jones",
    },
    {
        "name": "Tom Aspinall",
        "nickname": "",
        "weight_class": "Heavyweight",
        "nationality": "United Kingdom",
        "record_wins": 15,
        "record_losses": 3,
        "record_draws": 0,
        "wins_ko_tko": 11,
        "wins_submission": 3,
        "wins_decision": 1,
        "losses_ko_tko": 2,
        "losses_submission": 1,
        "losses_decision": 0,
        "sig_strikes_per_min": 5.88,
        "strike_accuracy": 62.0,
        "takedown_avg": 2.50,
        "takedown_accuracy": 50.0,
        "takedown_defense": 66.0,
        "sub_attempts_per_min": 0.8,
        "sportradar_id": "sr:competitor:aspinall",
    },
    {
        "name": "Alex Pereira",
        "nickname": "Poatan",
        "weight_class": "Light Heavyweight",
        "nationality": "Brazil",
        "record_wins": 12,
        "record_losses": 2,
        "record_draws": 0,
        "wins_ko_tko": 10,
        "wins_submission": 0,
        "wins_decision": 2,
        "losses_ko_tko": 1,
        "losses_submission": 1,
        "losses_decision": 0,
        "sig_strikes_per_min": 5.71,
        "strike_accuracy": 57.0,
        "takedown_avg": 0.00,
        "takedown_accuracy": 0.0,
        "takedown_defense": 76.0,
        "sub_attempts_per_min": 0.0,
        "sportradar_id": "sr:competitor:pereira",
    },
    {
        "name": "Magomed Ankalaev",
        "nickname": "",
        "weight_class": "Light Heavyweight",
        "nationality": "Russia",
        "record_wins": 19,
        "record_losses": 1,
        "record_draws": 1,
        "wins_ko_tko": 9,
        "wins_submission": 1,
        "wins_decision": 9,
        "losses_ko_tko": 0,
        "losses_submission": 0,
        "losses_decision": 1,
        "sig_strikes_per_min": 3.50,
        "strike_accuracy": 51.0,
        "takedown_avg": 2.18,
        "takedown_accuracy": 55.0,
        "takedown_defense": 90.0,
        "sub_attempts_per_min": 0.1,
        "sportradar_id": "sr:competitor:ankalaev",
    },
    {
        "name": "Sean O'Malley",
        "nickname": "Sugar",
        "weight_class": "Bantamweight",
        "nationality": "United States",
        "record_wins": 18,
        "record_losses": 2,
        "record_draws": 0,
        "wins_ko_tko": 12,
        "wins_submission": 0,
        "wins_decision": 6,
        "losses_ko_tko": 1,
        "losses_submission": 0,
        "losses_decision": 1,
        "sig_strikes_per_min": 5.98,
        "strike_accuracy": 55.0,
        "takedown_avg": 0.40,
        "takedown_accuracy": 36.0,
        "takedown_defense": 72.0,
        "sub_attempts_per_min": 0.0,
        "sportradar_id": "sr:competitor:omalley",
    },
    {
        "name": "Merab Dvalishvili",
        "nickname": "The Machine",
        "weight_class": "Bantamweight",
        "nationality": "Georgia",
        "record_wins": 18,
        "record_losses": 4,
        "record_draws": 0,
        "wins_ko_tko": 3,
        "wins_submission": 2,
        "wins_decision": 13,
        "losses_ko_tko": 0,
        "losses_submission": 2,
        "losses_decision": 2,
        "sig_strikes_per_min": 5.03,
        "strike_accuracy": 44.0,
        "takedown_avg": 5.13,
        "takedown_accuracy": 34.0,
        "takedown_defense": 84.0,
        "sub_attempts_per_min": 0.3,
        "sportradar_id": "sr:competitor:dvalishvili",
    },
    {
        "name": "Dricus du Plessis",
        "nickname": "Stillknocks",
        "weight_class": "Middleweight",
        "nationality": "South Africa",
        "record_wins": 22,
        "record_losses": 2,
        "record_draws": 0,
        "wins_ko_tko": 14,
        "wins_submission": 5,
        "wins_decision": 3,
        "losses_ko_tko": 1,
        "losses_submission": 1,
        "losses_decision": 0,
        "sig_strikes_per_min": 6.50,
        "strike_accuracy": 56.0,
        "takedown_avg": 2.00,
        "takedown_accuracy": 47.0,
        "takedown_defense": 62.0,
        "sub_attempts_per_min": 0.7,
        "sportradar_id": "sr:competitor:duplessis",
    },
    {
        "name": "Sean Strickland",
        "nickname": "Tarzan",
        "weight_class": "Middleweight",
        "nationality": "United States",
        "record_wins": 29,
        "record_losses": 6,
        "record_draws": 0,
        "wins_ko_tko": 12,
        "wins_submission": 4,
        "wins_decision": 13,
        "losses_ko_tko": 4,
        "losses_submission": 1,
        "losses_decision": 1,
        "sig_strikes_per_min": 5.68,
        "strike_accuracy": 49.0,
        "takedown_avg": 0.97,
        "takedown_accuracy": 31.0,
        "takedown_defense": 82.0,
        "sub_attempts_per_min": 0.1,
        "sportradar_id": "sr:competitor:strickland",
    },
]

print("Seeding fighters...")
fighters = {}
for data in fighters_data:
    fighter, created = Fighter.objects.update_or_create(
        sportradar_id=data.pop("sportradar_id"),
        defaults=data,
    )
    fighters[fighter.name] = fighter
    status = "created" if created else "updated"
    print(f"  {status}: {fighter}")

# --- Event ---

print("\nSeeding events...")
event, created = Event.objects.update_or_create(
    sportradar_id="sr:event:ufc310",
    defaults={
        "name": "UFC 310: Makhachev vs Volkanovski 2",
        "date": datetime(2025, 7, 12, 22, 0, tzinfo=timezone.utc),
        "location": "Las Vegas, Nevada",
        "venue": "T-Mobile Arena",
        "status": "completed",
    },
)
print(f"  {'created' if created else 'updated'}: {event}")

# --- Fights ---

print("\nSeeding fights...")
fights_data = [
    {
        "fighter_a": "Islam Makhachev",
        "fighter_b": "Alexander Volkanovski",
        "weight_class": "Lightweight",
        "card_section": "main",
        "order": 0,
    },
    {
        "fighter_a": "Alex Pereira",
        "fighter_b": "Magomed Ankalaev",
        "weight_class": "Light Heavyweight",
        "card_section": "main",
        "order": 1,
    },
    {
        "fighter_a": "Sean O'Malley",
        "fighter_b": "Merab Dvalishvili",
        "weight_class": "Bantamweight",
        "card_section": "main",
        "order": 2,
    },
    {
        "fighter_a": "Dricus du Plessis",
        "fighter_b": "Sean Strickland",
        "weight_class": "Middleweight",
        "card_section": "prelim",
        "order": 0,
    },
    {
        "fighter_a": "Jon Jones",
        "fighter_b": "Tom Aspinall",
        "weight_class": "Heavyweight",
        "card_section": "prelim",
        "order": 1,
    },
]

for data in fights_data:
    fight, created = Fight.objects.update_or_create(
        event=event,
        fighter_a=fighters[data["fighter_a"]],
        fighter_b=fighters[data["fighter_b"]],
        defaults={
            "weight_class": data["weight_class"],
            "card_section": data["card_section"],
            "order": data["order"],
        },
    )
    status = "created" if created else "updated"
    print(f"  {status}: {fight}")

print(f"\nDone! {Fighter.objects.count()} fighters, {Event.objects.count()} events, {Fight.objects.count()} fights in DB.")
