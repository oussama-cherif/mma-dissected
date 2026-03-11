from django.test import TestCase
from django.utils import timezone
from .models import Event, Fight
from fighters.models import Fighter


class EventModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="UFC 326",
            date=timezone.now(),
            location="Las Vegas, NV",
            status="upcoming",
            sportradar_id="test-event-326",
        )

    def test_str_representation(self):
        self.assertIn("UFC 326", str(self.event))

    def test_fight_count(self):
        self.assertEqual(self.event.fight_count, 0)


class FightModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="UFC 326",
            date=timezone.now(),
            sportradar_id="test-event-326",
        )
        self.fighter_a = Fighter.objects.create(
            name="Fighter A",
            weight_class="Lightweight",
            sportradar_id="test-a-001",
            record_wins=10,
            record_losses=2,
        )
        self.fighter_b = Fighter.objects.create(
            name="Fighter B",
            weight_class="Lightweight",
            sportradar_id="test-b-001",
            record_wins=8,
            record_losses=4,
        )
        self.fight = Fight.objects.create(
            event=self.event,
            fighter_a=self.fighter_a,
            fighter_b=self.fighter_b,
            weight_class="Lightweight",
            card_section="main",
            order=1,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.fight), "Fighter A vs Fighter B")

    def test_fight_count_updates(self):
        self.assertEqual(self.event.fight_count, 1)


class EventAPITest(TestCase):
    def setUp(self):
        Event.objects.create(
            name="UFC 326",
            date=timezone.now(),
            location="Las Vegas, NV",
            status="upcoming",
            sportradar_id="test-event-326",
        )

    def test_event_list(self):
        response = self.client.get("/api/events/")
        self.assertEqual(response.status_code, 200)

    def test_event_detail(self):
        event = Event.objects.first()
        response = self.client.get(f"/api/events/{event.id}/")
        self.assertEqual(response.status_code, 200)
