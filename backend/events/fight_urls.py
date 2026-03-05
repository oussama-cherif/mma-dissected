from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FightViewSet

router = DefaultRouter()
router.register("", FightViewSet, basename="fight")

urlpatterns = [
    path("", include(router.urls)),
]
