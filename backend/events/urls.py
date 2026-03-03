from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, FightViewSet

router = DefaultRouter()
router.register("", EventViewSet, basename="event")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:event_pk>/fights/<int:pk>/", FightViewSet.as_view({"get": "retrieve"}), name="fight-detail"),
]
