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
