<template>
  <div class="wrapper">
    <q-card>
      <q-card-section>
        <apexchart
          :height="height"
          :width="width"
          :options="chartOptions"
          :series="chartSeries"
        />
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "HistoricalPortfolioValueChart",
  methods: {
    fetchData() {
      if (this.$store.getters["core/getPeriod"].value === "-") return;
      this.$axios
        .get(
          `/api/cik/${this.cik}/portfolio/${this.$store.getters["core/getPeriod"].value}/`,
          { params: { chart: true } }
        )
        .then(resp => {
          this.results = resp.data.results;
        });
    }
  },
  props: {
    cik: {
      type: String,
      default: ""
    },
    height: {
      type: Number,
      default: 300
    },
    width: {
      type: String,
      default: "100%"
    }
  },
  created() {
    this.fetchData();
  },
  watch: {
    period(newValue, oldValue) {
      this.fetchData();
    }
  },
  computed: {
    ...mapState("core", ["period"]),
    resultsData() {
      return this.results;
    },
    totals() {
      return this.results.map(x => x.total) || [];
    },
    chartLabels() {
      return this.results.map(x => x.cusip_number) || [];
    },
    chartOptions() {
      return {
        chart: {
          height: 350,
          animations: {
            enabled: false
          }
        },
        theme: {
          mode: "light"
        },
        stroke: {
          width: [0, 4]
        },
        title: {
          text: `Top 100 Holdings by Value ${this.$store.getters["core/getPeriod"].label}`
        },
        dataLabels: {
          enabled: true,
          enabledOnSeries: [1]
        },
        labels: this.chartLabels,
        // xaxis: {
        //   type: "datetime"
        // },
        yaxis: {
          forceNiceScale: true,
          min: 0,
          title: {
            text: "Value"
          }
        }
      };
    },
    chartSeries() {
      return [
        {
          name: "Value",
          type: "column",
          data: this.totals
        }
      ];
    }
  },
  data() {
    return {
      results: []
    };
  }
};
</script>

<style>
.wrapper {
  margin-bottom: 10px;
}
</style>
