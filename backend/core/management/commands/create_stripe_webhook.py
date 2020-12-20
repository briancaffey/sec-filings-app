import logging
import os


import stripe
from django.core.management.base import BaseCommand

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)

stripe.api_key = os.environ.get("STRIPE_API_KEY")


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        This management command creates a webhook in Stripe.

        This is only used in production. In development, use:
            stripe listen --forward-to localhost/api/stripe-webhooks/

        Once the webhook is create, STRIPE_WEBHOOK_SECRET needs to be added
        to environment variables
        """

        logger.info("Creating Stripe Webhook")

        stripe.WebhookEndpoint.create(
            url="https://opensecdata.ga/api/stripe-webhooks/",
            enabled_events=["*"],
        )

        logger.info("Created Stripe Webhook")
