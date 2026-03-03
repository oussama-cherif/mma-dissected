from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Event, Fight
from .serializers import (
    EventListSerializer,
    EventDetailSerializer,
    FightDetailSerializer,
)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EventDetailSerializer
        return EventListSerializer

    @action(detail=False, methods=["get"])
    def next(self, request):
        """Return the next upcoming UFC event."""
        upcoming = Event.objects.filter(
            status="upcoming", date__gte=timezone.now()
        ).order_by("date").first()

        if not upcoming:
            return Response({"detail": "No upcoming events found."}, status=404)

        serializer = EventDetailSerializer(upcoming)
        return Response(serializer.data)


class FightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fight.objects.select_related("fighter_a", "fighter_b", "winner")
    serializer_class = FightDetailSerializer
