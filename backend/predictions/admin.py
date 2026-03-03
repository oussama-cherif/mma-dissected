from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ["fight", "predicted_winner", "confidence", "created_at"]
    list_filter = ["confidence"]
    readonly_fields = ["created_at"]
