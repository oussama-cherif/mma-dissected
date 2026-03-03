from rest_framework import serializers
from .models import Prediction
from fighters.serializers import FighterListSerializer


class PredictionSerializer(serializers.ModelSerializer):
    predicted_winner = FighterListSerializer(read_only=True)

    class Meta:
        model = Prediction
        fields = [
            "id",
            "fight",
            "predicted_winner",
            "confidence",
            "prob_ko_tko",
            "prob_submission",
            "prob_dec_unanimous",
            "prob_dec_split",
            "prob_dec_majority",
            "predicted_round",
            "predicted_time",
            "key_factors",
            "vulnerability_note",
            "betting_insight",
            "created_at",
        ]
