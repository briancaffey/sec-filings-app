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
    <q-btn
      type="a"
      :href="
        `/api/funds/scatterplot/${$store.getters['core/getPeriod'].value}/`
      "
      ><code>API</code></q-btn
    >
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "HistoricalPortfolioValueChart",
  methods: {
    fetchData() {
      if (this.period !== "-") {
        if (this.$store.getters["core/getPeriod"].value === "-") return;
        this.$axios
          .get(`/api/funds/scatterplot/${this.period.value}/`)
          .then(resp => {
            this.results = resp.data;
          });
      }
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
    funds() {
      return this.results.map(x => {
        return {
          x: x.holding_count,
          y: x.fund_size,
          cik_number: x.cik_number,
          filer_name: x.filer_name
        };
      });
    },
    totals() {
      return this.results.map(x => x.total) || [];
    },
    chartOptions() {
      const currency = this.$options.filters.currency;
      const vm = this;
      return {
        chart: {
          events: {
            click: function(event, chartContext, config) {
              vm.$router.push(
                `/cik/${vm.funds[config.dataPointIndex].cik_number}`
              );
            }
          },
          animations: {
            enabled: false
          },
          height: 350,
          type: "scatter",
          zoom: {
            enabled: true,
            type: "xy"
          }
        },
        theme: {
          mode: "light"
        },
        stroke: {
          width: [0, 4]
        },
        title: {
          text: `Fund sizes (${this.$store.getters["core/getPeriod"].label})`
        },
        xaxis: {
          title: {
            text: "Holding Count"
          },
          tickAmount: 10
        },
        yaxis: {
          forceNiceScale: true,
          min: 0,
          title: {
            text: "Value"
          }
        },
        tooltip: {
          x: {
            show: true,
            formatter: function(value, opts) {
              return (
                "Holdings: " +
                opts.w.config.series[opts.seriesIndex].data[opts.dataPointIndex]
                  .x
              );
            }
          },
          y: {
            show: false,
            formatter: function(value, opts) {
              return (
                "$" +
                currency(opts.series[opts.seriesIndex][opts.dataPointIndex]) +
                " - " +
                opts.w.config.series[opts.seriesIndex].data[opts.dataPointIndex]
                  .filer_name
              );
            }
          }
        }
      };
    },
    chartSeries() {
      return [
        {
          name: "Company",
          data: this.funds
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
