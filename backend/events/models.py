from django.db import models


class Event(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("live", "Live"),
        ("completed", "Completed"),
    ]

    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, default="")
    venue = models.CharField(max_length=200, blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")
    sportradar_id = models.CharField(max_length=100, unique=True)
    last_synced = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.name} — {self.date.strftime('%b %d, %Y')}"

    @property
    def fight_count(self):
        return self.fights.count()


class Fight(models.Model):
    CARD_SECTION_CHOICES = [
        ("main", "Main Card"),
        ("co-main", "Co-Main"),
        ("prelim", "Prelims"),
        ("early", "Early Prelims"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="fights")
    fighter_a = models.ForeignKey(
        "fighters.Fighter", on_delete=models.CASCADE, related_name="fights_as_a"
    )
    fighter_b = models.ForeignKey(
        "fighters.Fighter", on_delete=models.CASCADE, related_name="fights_as_b"
    )
    weight_class = models.CharField(max_length=50)
    card_section = models.CharField(max_length=20, choices=CARD_SECTION_CHOICES, default="main")
    order = models.IntegerField(default=0)
    winner = models.ForeignKey(
        "fighters.Fighter",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fights_won",
    )
    method = models.CharField(max_length=50, blank=True, default="")
    final_round = models.IntegerField(null=True, blank=True)
    final_time = models.CharField(max_length=10, blank=True, default="")

    class Meta:
        ordering = ["card_section", "order"]

    def __str__(self):
        return f"{self.fighter_a.name} vs {self.fighter_b.name}"
