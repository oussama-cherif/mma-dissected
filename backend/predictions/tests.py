from django.test import TestCase
from django.utils import timezone
from fighters.models import Fighter
from events.models import Event, Fight
from .models import Prediction
from .predictor import generate_stats_prediction, save_prediction, generate_prediction


class PredictorTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="UFC 326",
            date=timezone.now(),
            sportradar_id="test-event-pred",
        )
        self.striker = Fighter.objects.create(
            name="Heavy Hitter",
            weight_class="Heavyweight",
            sportradar_id="test-striker-001",
            record_wins=15,
            record_losses=3,
            wins_ko_tko=12,
            wins_submission=1,
            wins_decision=2,
            losses_ko_tko=1,
            losses_submission=1,
            losses_decision=1,
            sig_strikes_per_min=6.5,
            strike_accuracy=55.0,
            takedown_avg=0.5,
            takedown_defense=70.0,
        )
        self.grappler = Fighter.objects.create(
            name="Ground Master",
            weight_class="Heavyweight",
            sportradar_id="test-grappler-001",
            record_wins=20,
            record_losses=4,
            wins_ko_tko=2,
            wins_submission=12,
            wins_decision=6,
            losses_ko_tko=3,
            losses_submission=0,
            losses_decision=1,
            sig_strikes_per_min=3.2,
            strike_accuracy=45.0,
            takedown_avg=4.5,
            takedown_defense=85.0,
            sub_attempts_per_min=1.8,
        )
        self.fight = Fight.objects.create(
            event=self.event,
            fighter_a=self.striker,
            fighter_b=self.grappler,
            weight_class="Heavyweight",
            card_section="main",
            order=1,
        )

    def test_prediction_returns_valid_structure(self):
        result = generate_stats_prediction(self.fight)
        self.assertIn("winner", result)
        self.assertIn("confidence", result)
        self.assertIn("method_probabilities", result)
        self.assertIn("key_factors", result)
        self.assertIn("vulnerability_note", result)
        self.assertIn("betting_insight", result)

    def test_confidence_in_range(self):
        result = generate_stats_prediction(self.fight)
        self.assertGreaterEqual(result["confidence"], 50)
        self.assertLessEqual(result["confidence"], 95)

    def test_method_probabilities_sum_to_100(self):
        result = generate_stats_prediction(self.fight)
        probs = result["method_probabilities"]
        total = (
            probs["ko_tko"]
            + probs["submission"]
            + probs["decision_unanimous"]
            + probs["decision_split"]
            + probs["decision_majority"]
        )
        self.assertEqual(total, 100)

    def test_winner_is_one_of_the_fighters(self):
        result = generate_stats_prediction(self.fight)
        self.assertIn(result["winner"], ["Heavy Hitter", "Ground Master"])

    def test_vulnerability_detected_ko(self):
        """Striker with 12 KO wins vs grappler with 3 KO losses should flag."""
        result = generate_stats_prediction(self.fight)
        self.assertIn("KO/TKO", result["vulnerability_note"])

    def test_vulnerability_detected_submission(self):
        """Grappler with 12 sub wins vs striker with 1 sub loss — check threshold."""
        # 12 * 1 = 12 >= 2, and grappler has 12 sub wins >= 2
        result = generate_stats_prediction(self.fight)
        self.assertIn("submission", result["vulnerability_note"])

    def test_save_prediction_creates_record(self):
        result = generate_stats_prediction(self.fight)
        prediction = save_prediction(self.fight, result)
        self.assertIsInstance(prediction, Prediction)
        self.assertEqual(prediction.fight, self.fight)

    def test_generate_prediction_end_to_end(self):
        prediction = generate_prediction(self.fight)
        self.assertIsInstance(prediction, Prediction)
        self.assertGreaterEqual(prediction.confidence, 50)

    def test_key_factors_not_empty(self):
        result = generate_stats_prediction(self.fight)
        self.assertGreater(len(result["key_factors"]), 0)

    def test_betting_insight_generated_with_vulnerabilities(self):
        result = generate_stats_prediction(self.fight)
        # With high vulnerability severity, insight should be populated
        if result["vulnerability_note"]:
            self.assertNotEqual(result["betting_insight"], "")


class EvenMatchupTest(TestCase):
    """Test prediction with two similar fighters."""

    def setUp(self):
        self.event = Event.objects.create(
            name="UFC Test",
            date=timezone.now(),
            sportradar_id="test-event-even",
        )
        self.fighter_a = Fighter.objects.create(
            name="Fighter Alpha",
            weight_class="Welterweight",
            sportradar_id="test-alpha-001",
            record_wins=10,
            record_losses=5,
            wins_ko_tko=3,
            wins_submission=3,
            wins_decision=4,
            losses_ko_tko=2,
            losses_submission=1,
            losses_decision=2,
            sig_strikes_per_min=4.0,
            strike_accuracy=50.0,
            takedown_avg=2.0,
            takedown_defense=65.0,
        )
        self.fighter_b = Fighter.objects.create(
            name="Fighter Beta",
            weight_class="Welterweight",
            sportradar_id="test-beta-001",
            record_wins=10,
            record_losses=5,
            wins_ko_tko=3,
            wins_submission=3,
            wins_decision=4,
            losses_ko_tko=2,
            losses_submission=1,
            losses_decision=2,
            sig_strikes_per_min=4.0,
            strike_accuracy=50.0,
            takedown_avg=2.0,
            takedown_defense=65.0,
        )
        self.fight = Fight.objects.create(
            event=self.event,
            fighter_a=self.fighter_a,
            fighter_b=self.fighter_b,
            weight_class="Welterweight",
            card_section="main",
            order=1,
        )

    def test_even_matchup_close_confidence(self):
        result = generate_stats_prediction(self.fight)
        # Should be close to 50-50
        self.assertLessEqual(result["confidence"], 60)


class PredictionAPITest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="UFC 326",
            date=timezone.now(),
            sportradar_id="test-event-api",
        )
        self.fighter_a = Fighter.objects.create(
            name="Test Fighter A",
            weight_class="Lightweight",
            sportradar_id="test-api-a",
            record_wins=10,
        )
        self.fighter_b = Fighter.objects.create(
            name="Test Fighter B",
            weight_class="Lightweight",
            sportradar_id="test-api-b",
            record_wins=8,
        )
        self.fight = Fight.objects.create(
            event=self.event,
            fighter_a=self.fighter_a,
            fighter_b=self.fighter_b,
            weight_class="Lightweight",
        )

    def test_generate_prediction_via_api(self):
        response = self.client.post(
            f"/api/predictions/fights/{self.fight.id}/prediction/"
        )
        self.assertIn(response.status_code, [200, 201])
        self.assertIn("predicted_winner", response.json())

    def test_get_prediction_after_generation(self):
        generate_prediction(self.fight)
        response = self.client.get(
            f"/api/predictions/fights/{self.fight.id}/prediction/"
        )
        self.assertEqual(response.status_code, 200)
