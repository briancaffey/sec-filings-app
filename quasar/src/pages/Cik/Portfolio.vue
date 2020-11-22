<template>
  <q-page padding>
    <portfolio-summary :cik="$route.params.cik" />
    <portfolio-holdings-by-period-table :cik="$route.params.cik" />
    <portfolio-holdings-by-period-chart :cik="$route.params.cik" />
    <historical-portfolio-value-chart :cik="$route.params.cik" />
  </q-page>
</template>

<script>
export default {};
</script>

<style scoped></style>
