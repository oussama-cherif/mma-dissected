from django.db import models


class Fighter(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True, default="")
    weight_class = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, blank=True, default="")
    record_wins = models.IntegerField(default=0)
    record_losses = models.IntegerField(default=0)
    record_draws = models.IntegerField(default=0)
    wins_ko_tko = models.IntegerField(default=0)
    wins_submission = models.IntegerField(default=0)
    wins_decision = models.IntegerField(default=0)
    losses_ko_tko = models.IntegerField(default=0)
    losses_submission = models.IntegerField(default=0)
    losses_decision = models.IntegerField(default=0)
    avg_fight_time = models.FloatField(null=True, blank=True)
    sig_strikes_per_min = models.FloatField(null=True, blank=True)
    strike_accuracy = models.FloatField(null=True, blank=True)
    takedown_avg = models.FloatField(null=True, blank=True)
    takedown_accuracy = models.FloatField(null=True, blank=True)
    takedown_defense = models.FloatField(null=True, blank=True)
    sub_attempts_per_min = models.FloatField(null=True, blank=True)
    sportradar_id = models.CharField(max_length=100, unique=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.record_wins}-{self.record_losses}-{self.record_draws})"

    @property
    def record(self):
        return f"{self.record_wins}-{self.record_losses}-{self.record_draws}"

    @property
    def total_fights(self):
        return self.record_wins + self.record_losses + self.record_draws
