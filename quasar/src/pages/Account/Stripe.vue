<template>
  <div>
    <div class="text-h6">Purchase Premium</div>
    <br />
    <div>
      A premium account gives you unlimited API access.
    </div>
    <br />
    <div style="max-width: 350px;">
      <div ref="card"></div>
    </div>
    <br />
    <q-btn color="primary" @click="purchase">Purchase</q-btn>
  </div>
</template>

<script>
let style = {
  base: {
    border: "1px solid #D8D8D8",
    borderRadius: "4px",
    color: "#000"
  },

  invalid: {
    // All of the error styles go inside of here.
  }
};
let stripe = Stripe(process.env.STRIPE_PUBLISHABLE_KEY),
  elements = stripe.elements(),
  card = undefined;

export default {
  data() {
    return {
      stripeCustomerId: null
    };
  },
  created() {
    this.$axios.post("/api/stripe/create-customer/").then(resp => {
      console.log("stripe user created");
      this.stripeCustomerId = resp.data.stripe_customer_id;
    });
  },
  mounted: function() {
    card = elements.create("card", { style });
    card.mount(this.$refs.card);
  },
  methods: {
    createSubscription({ customerId, paymentMethodId, priceId }) {
      return (
        this.$axios
          .post(
            "/api/stripe/create-subscription/",
            {
              customerId: customerId,
              paymentMethodId: paymentMethodId,
              priceId: priceId
            },
            {
              headers: {
                "Content-type": "application/json"
              }
            }
          )
          .then(response => {
            return response;
          })
          // If the card is declined, display an error to the user.
          .then(result => {
            if (result.error) {
              // The card had an error when trying to attach it to a customer.
              throw result;
            }
            return result;
          })
          // Normalize the result to contain the object returned by Stripe.
          // Add the additional details we need.
          .then(result => {
            return {
              paymentMethodId: paymentMethodId,
              priceId: priceId,
              subscription: result
            };
          })
        // // Some payment methods require a customer to be on session
        // // to complete the payment process. Check the status of the
        // // payment intent to handle these actions.
        // .then(handlePaymentThatRequiresCustomerAction)
        // // If attaching this card to a Customer object succeeds,
        // // but attempts to charge the customer fail, you
        // // get a requires_payment_method error.
        // .then(handleRequiresPaymentMethod)
        // // No more actions required. Provision your service for the user.
        // .then(onSubscriptionComplete)
        // .catch(error => {
        //   // An error has happened. Display the failure to the user here.
        //   // We utilize the HTML element we created.
        //   showCardError(error);
        // })
      );
    },
    purchase() {
      stripe
        .createPaymentMethod({
          type: "card",
          card: card
        })
        .then(result => {
          if (result.error) {
            console.log(result);
            alert(result);
          } else {
            this.createSubscription({
              customerId: this.stripeCustomerId,
              paymentMethodId: result.paymentMethod.id,
              priceId: "price_1Hx0goL67dRDwyuDh9yEWsBo"
            });
          }
        });
    }
  }
};
</script>

<style>
.StripeElement {
  box-sizing: border-box;

  height: 40px;

  padding: 10px 12px;

  border: 1px solid transparent;
  border-radius: 4px;
  background-color: white;

  box-shadow: 0 1px 3px 0 #e6ebf1;
  -webkit-transition: box-shadow 150ms ease;
  transition: box-shadow 150ms ease;
}

.StripeElement--focus {
  box-shadow: 0 1px 3px 0 #cfd7df;
}

.StripeElement--invalid {
  border-color: #fa755a;
}

.StripeElement--webkit-autofill {
  background-color: #fefde5 !important;
}
</style>
