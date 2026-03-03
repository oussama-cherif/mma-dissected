from django.contrib import admin
from .models import Event, Fight


class FightInline(admin.TabularInline):
    model = Fight
    extra = 0
    raw_id_fields = ["fighter_a", "fighter_b", "winner"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "date", "location", "status"]
    list_filter = ["status"]
    search_fields = ["name", "location"]
    inlines = [FightInline]


@admin.register(Fight)
class FightAdmin(admin.ModelAdmin):
    list_display = ["__str__", "event", "weight_class", "card_section"]
    list_filter = ["card_section", "weight_class"]
    raw_id_fields = ["fighter_a", "fighter_b", "winner"]
