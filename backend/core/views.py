from datetime import datetime
import json
import logging
import os


from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import stripe

from accounts.models import Subscription

User = get_user_model()

stripe.api_key = os.environ.get("STRIPE_API_KEY")

# two days in seconds
TWO_DAYS = 60 * 60 * 24 * 2

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


# Create your views here.
def health_check(request):
    response = JsonResponse({"message": "OK"})
    return response


@csrf_exempt
def stripe_webhooks(request):

    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        data = event["data"]
    except ValueError as e:
        logger.info(e)
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.info(e)
        # Invalid signature
        return HttpResponse(status=400)

    data_object = data["object"]
    event_type = json.loads(payload)["type"]

    logger.info(f"Event type: {event_type}")

    if event_type == "product.created":
        logger.info("Product created successfully.")

    if event_type == "product.deleted":
        logger.info("Product deleted successfully")

    if event_type == "invoice.paid":
        logger.info("Subscription invoice was paid")
        logger.info("Updating subscription...")

        # data.object is an invoice for events of type `invoice.paid`
        # We need to get the subscription id from this data object,
        # then update the valid_through date for this subscription
        subscription_id = data_object["lines"]["data"][0]["subscription"]
        current_period_end = data_object["lines"]["data"][0][
            "current_period_end"
        ]
        subscription = Subscription.objects.get(
            stripe_subscription_id=subscription_id
        )
        subscription.valid_through = current_period_end + TWO_DAYS
        subscription.save()
        logger.info("Subscription updated")

    logger.info("Finished processing Stripe Webhook")

    return HttpResponse(status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    try:
        # Cancel the subscription by deleting it
        logger.info("Cancelling subscription")

        # delete the subscription in Stripe
        logger.info("Cancelling subscription in Stripe")
        deleted_subscription = stripe.Subscription.delete(
            request.data['subscriptionId']
        )

        logger.info("Deleting subscription on user model")
        request.user.subscription.delete()
        return Response(deleted_subscription)
    except Exception as e:
        return Response({"message": str(e)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_subscription(request):

    data = request.data

    # run the `create_stripe_data` management command and get the price_id
    # from the Stripe console and add it to `.env` as SUBSCRIPTION_PRICE_ID
    price_id = os.environ.get("SUBSCRIPTION_PRICE_ID", "price_abc124")

    try:

        logger.info("Creating Stripe Customer")
        stripe_customer = stripe.Customer.create(email=request.user.email)
        logger.info("Stripe Customer created")
        if "id" in stripe_customer:
            stripe_customer_id = stripe_customer["id"]
        else:
            # what happens if Customer.create is called with
            # an email that already exists?
            return JsonResponse({"message": "Error creating Stripe Customer"})

        # Attach the payment method to the customer
        logger.info("Attaching payment info to customer")
        stripe.PaymentMethod.attach(
            data["paymentMethodId"], customer=stripe_customer_id,
        )

        # Set the default payment method on the customer
        logger.info("Setting default payment method for customer")
        stripe.Customer.modify(
            stripe_customer_id,
            invoice_settings={
                "default_payment_method": data["paymentMethodId"],
            },
        )

        # Create the subscription
        logger.info("Creating Stripe Subscription")
        stripe_subscription = stripe.Subscription.create(
            customer=stripe_customer_id,
            items=[{"price": price_id}],
            expand=["latest_invoice.payment_intent"],
        )

        # save the subscription to the user
        user = request.user

        logger.info("Creating Subscription (Django object)")
        subscription_object = Subscription(
            stripe_customer_id=stripe_customer_id,
            # leave a grace period of a few days before cancelling subscription
            valid_through=datetime.fromtimestamp(
                stripe_subscription["current_period_end"]
                + TWO_DAYS  # two days in seconds
            ),
            stripe_subscription_id=stripe_subscription["id"],
        )

        logger.info("Save subscription model")
        subscription_object.save()
        logger.info("Save subscription model to user")
        user.subscription = subscription_object
        user.save()

        return Response(stripe_subscription)
    except Exception as e:
        return Response({"message": str(e)})
