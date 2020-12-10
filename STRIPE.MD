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

## Setup

Let's start by following along with the tutorial. The first step is to install `stripe` in our project.

```
strip==2.55.1
```
