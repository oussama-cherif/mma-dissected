from django.test import TestCase
from .models import Fighter


class FighterModelTest(TestCase):
    def setUp(self):
        self.fighter = Fighter.objects.create(
            name="Islam Makhachev",
            weight_class="Lightweight",
            sportradar_id="test-islam-001",
            record_wins=26,
            record_losses=1,
            record_draws=0,
            wins_ko_tko=4,
            wins_submission=11,
            wins_decision=11,
            losses_ko_tko=0,
            losses_submission=0,
            losses_decision=1,
            sig_strikes_per_min=4.21,
            strike_accuracy=58.0,
            takedown_avg=3.48,
            takedown_defense=90.0,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.fighter), "Islam Makhachev (26-1-0)")

    def test_record_property(self):
        self.assertEqual(self.fighter.record, "26-1-0")

    def test_total_fights(self):
        self.assertEqual(self.fighter.total_fights, 27)

    def test_ordering(self):
        Fighter.objects.create(
            name="Alex Pereira",
            weight_class="Light Heavyweight",
            sportradar_id="test-alex-001",
        )
        fighters = Fighter.objects.all()
        self.assertEqual(fighters[0].name, "Alex Pereira")
        self.assertEqual(fighters[1].name, "Islam Makhachev")


class FighterAPITest(TestCase):
    def setUp(self):
        Fighter.objects.create(
            name="Khabib Nurmagomedov",
            weight_class="Lightweight",
            sportradar_id="test-khabib-001",
            record_wins=29,
            record_losses=0,
        )

    def test_fighter_list(self):
        response = self.client.get("/api/fighters/")
        self.assertEqual(response.status_code, 200)

    def test_fighter_detail(self):
        fighter = Fighter.objects.first()
        response = self.client.get(f"/api/fighters/{fighter.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Khabib Nurmagomedov")
