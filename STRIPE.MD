# Notes on Integrating Stripe for Processing Payments

This application will offer a premium subscription service that users can pay for with Stripe. Premium subscriptions will give users unlimited access to the API as well as access to certain parts of the web UI that regular users do not have access to.

Our application will have the following user tiers:

- Unauthenticated guest users
- Free tier users (signed up with LinkedIn)
- Premium users (signed up with LinkedIn and payed with Stripe)

Before looking at the Stripe API, here's a brief overview of what I would like to be able to do:

- Build a view where signed-up users can purchase a Premium Plan
- API access for a signed-up user will be determined by their premium subscription status (non-active, active, cancelled)
- Users can cancel their premium subscriptions at any time

## Resources

This seems like a good place to start: [https://stripe.com/docs/billing/subscriptions/fixed-price](https://stripe.com/docs/billing/subscriptions/fixed-price).

This example has a GitHub repo with [an example backend implementation in Flask](https://github.com/stripe-samples/subscription-use-cases/tree/master/fixed-price-subscriptions/server/python) that should be a good reference for doing something similar in Django.

For the frontend this repo has examples for vanilla JS as well as React. These may also be helpful for our implementation in Vue.

## Stripe business setup

First we will need to setup a business in Stripe in which we can create our service.

Once we have setup the account, we will want to add the `test` API keys to our `.env` file. For the production keys, we can add these to the backend and NGINX `Dockerfile`s using `ARG` and `ENV`, and we can also add them in the `docker build` commands of the `.gitlab-ci.yml` file.

## Setup

Let's start by following along with the tutorial. The first step is to install `stripe` in our project.

```
stripe==2.55.1
```

### Install Stripe CLI

https://stripe.com/docs/stripe-cli

### Setup webhook with Stripe Webhook API

We can create a Django management command for testing this.

```py
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

```

Using the Stripe CLI, we can run the following command:

```
stripe listen --forward-to localhost/api/stripe-webhooks/
```

This cause Stripe to forward events to our local Django application to listen for events.

### Stripe Webhook in our Django application

Next let's create the `/api/stripe-webhooks/` endpoint:

```py
@csrf_exempt
def stripe_webhooks(request):

    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        data = event['data']
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)


    data_object = data['object']
    event_type = payload['type']

    if event_type == "product.created":
        logger


    return HttpResponse(status=200)
```

### Creating a credit card form in our Vue.js application

Next let's create a credit card form using Stripe Elements. I'll follow along with [this DigitalOcean guide on using Stripe with Vue](https://www.digitalocean.com/community/tutorials/vuejs-stripe-elements-vue-integration).

Before we start, let's add our `STRIPE_PUBLISHABLE_KEY` to our Quasar application. We can add it to `.env` and `.env.template` and then add it to `quasar.conf.js` under then `build` section.

We also want to add this key to `.gitlab-ci.yml` and as an `ARG` and `ENV` entry in the production NGINX Dockerfile.

First I'll add the following `script` tag to `index.template.html`:

```html
<script src="https://js.stripe.com/v3/"></script>
```

To be continued...


## High-level Overview

Here's a high level overview of what we need to setup recurring billing for our users: 

### Stripe account

1. A Stripe account with a business setup in Stripe. 
1. test API keys in local development (publishable key in frontend, secret key on backend)
1. live API keys in GitLab secrets, .gitlab-ci.yml, Dockerfiles and `docker build` commands as `--build-arg`s

### Backend

1. `stripe` package installed from PyPI
1. `stripe listen --forward-to localhost/api/stripe-webhooks/` command running using CLI (the key shown in the output of this command must be added to the `STRIPE_WEBHOOK_SECRET`)
1. django management command to create prices and products
1. `dj-stripe` to sync Stripe data with Django models
1. endpoint for Stripe webhooks to listen for events that happen (this can be used with dj-stripe)
1. endpoint for `create_subscription`

### Frontend

1. Add stripe via CDN to `index.html`: `<script src="https://js.stripe.com/v3/"></script>`
1. Add a `Stripe.vue` component 

### Frontend `Stripe.vue` component

1. Instantiate `stripe` with `Stripe("PUBLISHABLE_KEY")`
1. Define `elements` as `stripe.elements()`
1. In the mounted hook, create and mount the `card` variable
1. Define a `purchase` function that is called on a button click when card information is filled out and the customer is ready to purhcase
1. Inside the `purchase` function, call `stripe.createPaymentMethod` that takes in the `card` information. When `createPaymentMethod` completes, call our custom `createSubscription` function. 

### `createSubscription` function

1. This function needs to take in the `paymentMethod.id` that we get from the `result` of `stripe.createPaymentMethod`
1. This function will `POST` to our Django backend's `/api/stripe/create-subscription/` route (`create_subscription`)

### `/api/stripe/create-subscription/` backend route

1. This function does three things:
1. get or create the Stripe Customer ID (which is stored on the user model; `request.user.stripe_customer_id`) using `stripe.Customer.create`
1. Attach the payment method to the customer with `stripe.PaymentMethod.attach`
1. Set the default payment method on the customer with `stripe.Customer.modify`
1. Create the subscription with `stripe.Subscription.create`
1. Finally, this view returns the results of `stripe.Subscription.create` (`JsonResponse(subscription)`). 
1. We may want to save additional information from the `subscription` on our User model, such as the expiration date, or update a `subscription_status` flag for checking permissions when accessing gated resources.

## Questions

1. Would `PaymentIntent` be appropriate to use here? I'm still not sure how this should be used. 
