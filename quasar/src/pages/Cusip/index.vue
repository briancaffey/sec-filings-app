<template>
  <q-page padding>
    <q-card>
      <q-card-section>
        Details for <strong>{{ $route.params.cusip }}</strong>
        {{ $store.getters["cusip/getCompanyName"] }}
      </q-card-section>
    </q-card>
    <br />
    <ciks-by-cusip-table />
    <cusip-historical-value-chart />
  </q-page>
</template>

<script>
import { mapState } from "vuex";
export default {
  methods: {
    fetchData() {
      const cusip = this.$route.params.cusip;
      this.$store.dispatch("cusip/fetchData", cusip);
    }
  },
  computed: {
    ...mapState("core", ["period"])
  },
  watch: {
    period(newValue, oldValue) {
      this.fetchData();
    }
  }
};
</script>

<style scoped></style>
