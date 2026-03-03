from rest_framework import serializers
from .models import Fighter


class FighterListSerializer(serializers.ModelSerializer):
    record = serializers.CharField(read_only=True)

    class Meta:
        model = Fighter
        fields = [
            "id",
            "name",
            "nickname",
            "weight_class",
            "nationality",
            "record",
            "record_wins",
            "record_losses",
            "record_draws",
        ]


class FighterDetailSerializer(serializers.ModelSerializer):
    record = serializers.CharField(read_only=True)
    total_fights = serializers.IntegerField(read_only=True)

    class Meta:
        model = Fighter
        fields = "__all__"
