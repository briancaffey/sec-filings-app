<template>
  <q-page padding>
    <q-card>
      <q-card-section
        v-if="!$store.getters['user/getAccountStatus'].subscription"
      >
        <Stripe />
      </q-card-section>
      <q-card-section v-else>
        <Cancel />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import Stripe from "./Stripe";
import Cancel from "./Cancel";
export default {
  components: {
    Cancel,
    Stripe
  }
};
</script>

<style></style>
