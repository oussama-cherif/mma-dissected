from rest_framework import serializers
from .models import Event, Fight
from fighters.serializers import FighterListSerializer
from predictions.serializers import PredictionSerializer


class FightListSerializer(serializers.ModelSerializer):
    fighter_a = FighterListSerializer(read_only=True)
    fighter_b = FighterListSerializer(read_only=True)
    winner_id = serializers.PrimaryKeyRelatedField(source="winner", read_only=True)
    prediction = PredictionSerializer(read_only=True)

    class Meta:
        model = Fight
        fields = [
            "id",
            "fighter_a",
            "fighter_b",
            "weight_class",
            "card_section",
            "order",
            "winner_id",
            "method",
            "final_round",
            "final_time",
            "prediction",
        ]


class FightDetailSerializer(serializers.ModelSerializer):
    from fighters.serializers import FighterDetailSerializer

    fighter_a = FighterDetailSerializer(read_only=True)
    fighter_b = FighterDetailSerializer(read_only=True)
    winner_id = serializers.PrimaryKeyRelatedField(source="winner", read_only=True)

    class Meta:
        model = Fight
        fields = "__all__"


class EventListSerializer(serializers.ModelSerializer):
    fight_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ["id", "name", "date", "location", "venue", "status", "fight_count", "last_synced"]


class EventDetailSerializer(serializers.ModelSerializer):
    fights = FightListSerializer(many=True, read_only=True)
    fight_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date",
            "location",
            "venue",
            "status",
            "fight_count",
            "fights",
            "last_synced",
        ]
