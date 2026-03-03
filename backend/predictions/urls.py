from django.urls import path
from .views import FightPredictionView

fight_prediction = FightPredictionView.as_view({
    "get": "retrieve",
    "post": "create",
})

urlpatterns = [
    path("fights/<int:fight_pk>/prediction/", fight_prediction, name="fight-prediction"),
    path("fights/<int:fight_pk>/predict/", fight_prediction, name="fight-predict"),
]
