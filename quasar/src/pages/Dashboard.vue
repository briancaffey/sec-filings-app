<template>
  <div>
    <q-page padding>
      <q-card
        ><q-card-section
          >Holding Total: ${{
            $store.getters["dashboard/getHoldingsTotal"]
          }}</q-card-section
        ><q-card-section
          >Filing Count:
          {{ $store.getters["dashboard/getFilingCount"] }}</q-card-section
        >
        <q-card-section>
          Average Holding Value:
          {{
            $store.getters["dashboard/getAverageHoldingValue"]
          }}</q-card-section
        ></q-card
      ></q-page
    >
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
