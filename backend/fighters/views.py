from rest_framework import viewsets
from .models import Fighter
from .serializers import FighterListSerializer, FighterDetailSerializer


class FighterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fighter.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FighterDetailSerializer
        return FighterListSerializer
