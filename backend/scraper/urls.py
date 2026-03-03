from django.urls import path
from .views import ManualSyncView

urlpatterns = [
    path("card/", ManualSyncView.as_view(), name="manual-sync"),
]
