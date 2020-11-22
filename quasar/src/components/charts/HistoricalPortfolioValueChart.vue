<template>
  <div>
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
export default {
  name: "HistoricalPortfolioValueChart",
  methods: {
    fetchData() {
      this.$axios
        .get(`/api/cik/${this.cik}/portfolio/historical/`)
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
  computed: {
    resultsData() {
      return this.results;
    },
    values() {
      return this.results.map(x => x.value) || [];
    },
    chartLabels() {
      return this.results.map(x => x.filing_list__quarter) || [];
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
          width: [2, 4]
        },
        title: {
          text: "Historical Portfolio Value"
        },
        dataLabels: {
          enabled: true,
          enabledOnSeries: [1]
        },
        labels: this.chartLabels,
        xaxis: {
          type: "datetime"
        },
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
          // type: "line",
          data: this.values
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
