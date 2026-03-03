import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

BASE_URL = "https://api.sportradar.com/mma/trial/v2/en"


class SportRadarClient:
    """Client for fetching MMA data from the SportRadar API."""

    def __init__(self):
        self.api_key = settings.SPORTRADAR_API_KEY
        if not self.api_key:
            logger.warning("SPORTRADAR_API_KEY is not set")

    def _get(self, endpoint, params=None):
        """Make an authenticated GET request to the SportRadar API."""
        url = f"{BASE_URL}/{endpoint}"
        default_params = {"api_key": self.api_key}
        if params:
            default_params.update(params)

        response = requests.get(url, params=default_params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_schedule(self):
        """Fetch the upcoming MMA event schedule."""
        return self._get("schedule.json")

    def get_event(self, event_id):
        """Fetch details for a specific event."""
        return self._get(f"events/{event_id}/summary.json")

    def get_fighter_profile(self, fighter_id):
        """Fetch a fighter's full profile and stats."""
        return self._get(f"competitors/{fighter_id}/profile.json")
