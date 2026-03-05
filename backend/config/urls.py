from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/fighters/", include("fighters.urls")),
    path("api/events/", include("events.urls")),
    path("api/fights/", include("events.fight_urls")),
    path("api/predictions/", include("predictions.urls")),
    path("api/sync/", include("scraper.urls")),
    path("api/health/", health_check, name="health-check"),
]
