<template>
  <div>
    <q-page padding>
      <a href="/api/dashboard" style="text-decoration: none; color: black;">
        <q-card
          ><q-card-section
            >Holding Total: ${{
              $store.getters["dashboard/getHoldingsTotal"] | currency
            }}</q-card-section
          ><q-card-section
            >Filing Count:
            {{
              $store.getters["dashboard/getFilingCount"] | currency
            }}</q-card-section
          >
          <q-card-section>
            Average Holding Value: ${{
              $store.getters["dashboard/getAverageHoldingValue"] | currency
            }}</q-card-section
          ></q-card
        >
      </a>
    </q-page>
  </div>
</template>

<script>
export default {
  created() {
    this.$store.dispatch("dashboard/fetchData");
  }
};
</script>

<style scoped></style>
