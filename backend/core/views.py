import json
import logging
import os

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import stripe

stripe.api_key = os.environ.get("STRIPE_API_KEY")

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
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        data = event["data"]
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    data_object = data["object"]
    event_type = json.loads(payload)["type"]

    if event_type == "product.created":
        logger.info("Product created successfully.")

    if event_type == "product.deleted":
        logger.info("Product deleted successfully")

    logger.info("Finished processing Stripe Webhook")

    return HttpResponse(status=200)


def create_stripe_customer(request):
    stripe_customer_id = request.user.stripe_customer_id

    if not stripe_customer_id:
        logger.info(f"Creating Stripe User with email: {request.user.email}")
        stripe_customer = stripe.Customer.create(email=request.user.email)
        stripe_customer_id = stripe_customer["id"]

    return JsonResponse({"stripe_customer_id": stripe_customer_id})


def create_subscription(request):

    data = json.loads(request.body)

    try:
        # Attach the payment method to the customer
        stripe.PaymentMethod.attach(
            data["paymentMethodId"], customer=data["customerId"],
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(
            data["customerId"],
            invoice_settings={"default_payment_method": data["paymentMethodId"],},
        )

        # Create the subscription
        subscription = stripe.Subscription.create(
            customer=data["customerId"],
            items=[{"price": data["priceId"]}],
            expand=["latest_invoice.payment_intent"],
        )
        return JsonResponse(subscription)
    except Exception as e:
        return JsonResponse({"message": str(e)})

