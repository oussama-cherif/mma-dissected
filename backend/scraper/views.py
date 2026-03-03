from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .card_fetcher import sync_upcoming_events


class ManualSyncView(APIView):
    """Manually trigger a card sync."""

    def post(self, request):
        try:
            events = sync_upcoming_events()
            return Response(
                {"detail": f"Synced {len(events)} events.", "count": len(events)},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": f"Sync failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
