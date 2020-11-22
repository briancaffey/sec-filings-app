<template>
  <q-page padding>
    <q-card>
      <q-card-section>
        Details for <strong>{{ $route.params.cusip }}</strong> (<code
          ><a
            :href="
              `/api/cusip/${$route.params.cusip}/${$store.getters['core/getPeriod'].value}/`
            "
            >/api/cusip/{{ $route.params.cusip }}/{{
              $store.getters["core/getPeriod"].value
            }}/</a
          ></code
        >)
        {{ $store.getters["cusip/getCompanyName"] }}
      </q-card-section>
    </q-card>
    <br />
    <ciks-by-cusip-table />
  </q-page>
</template>

<script>
import { mapState } from "vuex";
export default {
  methods: {
    fetchData() {
      const cusip = this.$route.params.cusip;
      this.$store.dispatch("cusip/fetchData", cusip);
      this.$store.dispatch("cusip/historical/fetchData", { cusip });
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
