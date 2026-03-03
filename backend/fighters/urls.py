from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FighterViewSet

router = DefaultRouter()
router.register("", FighterViewSet, basename="fighter")

urlpatterns = [
    path("", include(router.urls)),
]
