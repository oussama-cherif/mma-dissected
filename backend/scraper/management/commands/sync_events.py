from django.core.management.base import BaseCommand
from scraper.card_fetcher import sync_upcoming_events


class Command(BaseCommand):
    help = "Scrape UFC events and fighter stats from ufcstats.com"

    def handle(self, *args, **options):
        self.stdout.write("Scraping ufcstats.com...")
        events = sync_upcoming_events()
        self.stdout.write(self.style.SUCCESS(
            f"Done. Synced {len(events)} events."
        ))
        for event in events:
            fights = event.fights.count()
            self.stdout.write(f"  - {event.name}: {fights} fights")
