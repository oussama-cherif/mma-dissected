from django.contrib import admin
from .models import Fighter


@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    list_display = ["name", "weight_class", "record_wins", "record_losses", "record_draws"]
    list_filter = ["weight_class"]
    search_fields = ["name", "nickname"]
