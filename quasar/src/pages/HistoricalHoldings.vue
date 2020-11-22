<template>
  <q-page padding>
    <q-card>
      <q-card-section>
        <historical-holdings-chart
          :cik="$route.params.cik"
          :cusip="$route.params.cusip"
        >
        </historical-holdings-chart>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
export default {};
</script>
