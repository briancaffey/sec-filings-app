import logging
import os


import stripe
from django.core.management.base import BaseCommand

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)

stripe.api_key = os.environ.get("STRIPE_API_KEY")


class Command(BaseCommand):
    def handle(self, *args, **options):
        PRODUCT_NAME = "Open SEC Data Premium Subscription"

        logger.info("Creating Stripe Product")
        product = stripe.Product.create(name=PRODUCT_NAME)

        product_id = product["id"]

        logger.info("Creating Stripe Price")
        stripe.Price.create(
            unit_amount=2000,
            currency="usd",
            recurring={"interval": "month"},
            product=product_id,
        )
        logger.info("Finished creating Stripe subscription data.")
