from django.urls import path

from . import views

urlpatterns = [
    path("health-check/", views.health_check, name="health-check"),
]
