<template>
  <q-card class="wrapper">
    <q-card-section>
      <div class="text-h6">
        {{ companyName }}
        <small style="color: grey"> ({{ $route.params.cik }}) </small>
        <q-separator class="sep" />
      </div>
      <div class="summary">
        <q-card>
          <q-card-section>
            <div>
              Total Value
            </div>
            <div class="text-h6" style="color: green;">
              <b>${{ (summary.total_value * 1000) | currency }}</b>
            </div>
          </q-card-section>
        </q-card>
        <q-card>
          <q-card-section>
            <div>
              Holdings
            </div>
            <div class="text-h6">
              <b>{{ summary.total_holdings | currency }}</b>
            </div>
          </q-card-section>
        </q-card>
        <q-card>
          <q-card-section>
            Quarter
            <div class="text-h6">
              {{ $store.getters["core/getPeriod"].label }}
            </div>
          </q-card-section>
        </q-card>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      companyName: "",
      summary: {
        total_value: null,
        total_holdings: null
      },
      previousPeriodSummary: {
        total_value: null,
        total_holdings: null
      },
      changes: {
        value_change: null,
        value_percent_change: null
      }
    };
  },
  watch: {
    period(newValue, oldValue) {
      this.fetchSummary();
    }
  },
  computed: {
    ...mapState("core", ["period"])
  },
  methods: {
    fetchSummary() {
      this.$axios
        .get(`/api/cik/${this.cik}/portfolio/summary/${this.period.value}/`)
        .then(resp => {
          this.companyName = resp.data.company_name;
          this.summary = resp.data.summary;
          this.previousPeriodSummary = resp.data.previous_period_summary;
          this.changes = resp.data.changes;
        });
    }
  },
  props: {
    cik: {
      type: String,
      default: null
    }
  }
};
</script>

<style scoped>
.summary {
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
}
.sep {
  margin-bottom: 10px;
}

.wrapper {
  margin-bottom: 10px;
}
</style>
