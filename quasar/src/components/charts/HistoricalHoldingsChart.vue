<template>
  <apexchart
    :height="height"
    :width="width"
    :options="chartOptions"
    :series="chartSeries"
  />
</template>

<script>
export default {
  name: "HistoricalHoldingsChart",
  methods: {
    fetchData() {
      this.$axios
        .get(`/api/holdings/${this.cik}/historical/${this.cusip}/`)
        .then(resp => {
          this.results = resp.data.results;
          this.companyName = resp.data.company_name;
        });
    }
  },
  props: {
    cik: {
      type: String,
      default: ""
    },
    cusip: {
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
    chartTitle() {
      return `Historical Holdings for ${this.companyName}`;
    },
    resultsData() {
      return this.results;
    },
    shares() {
      return this.results.map(x => x.sshPrnamt) || [];
    },
    values() {
      return this.results.map(x => x.value) || [];
    },
    chartLabels() {
      return this.results.map(x => x.filing__date_filed) || [];
    },
    chartOptions() {
      return {
        chart: {
          height: 350,
          animations: {
            enabled: false
          }
        },
        animations: {
          enabled: false
        },
        theme: {
          mode: "light"
        },
        stroke: {
          width: [0, 4]
        },
        title: {
          text: this.chartTitle
        },
        dataLabels: {
          enabled: true,
          enabledOnSeries: [1]
        },
        labels: this.chartLabels,
        xaxis: {
          type: "datetime"
        },
        yaxis: [
          {
            title: {
              text: "Shares"
            }
          },
          {
            opposite: true,
            title: {
              text: "Value"
            }
          }
        ]
      };
    },
    chartSeries() {
      return [
        {
          name: "Shares",
          type: "column",
          data: this.shares
        },
        {
          name: "Value",
          type: "line",
          data: this.values
        }
      ];
    }
  },
  data() {
    return {
      results: [],
      companyName: ""
    };
  }
};
</script>
