<template>
  <div>
    <q-btn @click="cancelSubscription" color="red"
      >Cancel My Premium Subscription</q-btn
    >
  </div>
</template>
<script>
export default {
  methods: {
    cancelSubscription() {
      const subscriptionId = this.$store.getters["user/getAccountStatus"]
        .subscription.stripe_subscription_id;
      this.$axios
        .post(
          "/api/stripe/cancel-subscription/",
          {
            subscriptionId: subscriptionId
          },
          {
            headers: {
              "Content-Type": "application/json"
            }
          }
        )
        .then(response => {
          console.log("Subscription cancelled.");
          this.$router.push("/account");
          this.$q.notify("Your subscription has been cancelled.");
        })
        .then(cancelSubscriptionResponse => {
          // Display to the user that the subscription has been cancelled.
        });
    }
  }
};
</script>
<style lang=""></style>
