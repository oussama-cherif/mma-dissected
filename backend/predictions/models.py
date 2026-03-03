from django.db import models


class Prediction(models.Model):
    fight = models.OneToOneField(
        "events.Fight", on_delete=models.CASCADE, related_name="prediction"
    )
    predicted_winner = models.ForeignKey(
        "fighters.Fighter", on_delete=models.CASCADE, related_name="predictions_won"
    )
    confidence = models.FloatField()
    prob_ko_tko = models.FloatField(default=0)
    prob_submission = models.FloatField(default=0)
    prob_dec_unanimous = models.FloatField(default=0)
    prob_dec_split = models.FloatField(default=0)
    prob_dec_majority = models.FloatField(default=0)
    predicted_round = models.IntegerField(null=True, blank=True)
    predicted_time = models.CharField(max_length=10, blank=True, default="")
    key_factors = models.JSONField(default=list)
    vulnerability_note = models.TextField(blank=True, default="")
    betting_insight = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction: {self.fight} → {self.predicted_winner.name} ({self.confidence}%)"
