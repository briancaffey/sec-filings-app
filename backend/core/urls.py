from django.urls import path

from . import views

urlpatterns = [
    path("health-check/", views.health_check, name="health-check"),
    path("stripe-webhooks/", views.stripe_webhooks, name="stripe-webhooks"),
    path(
        "stripe/create-subscription/",
        views.create_subscription,
        name="stripe-create-subscription",
    ),
    path(
        "stripe/cancel-subscription/",
        views.cancel_subscription,
        name="stripe-cancel-subscription",
    ),
]
