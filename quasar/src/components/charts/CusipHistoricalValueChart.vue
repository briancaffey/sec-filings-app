<template>
  <div>
    <br />
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
  computed: {
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
          text: "Historical Security Value"
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
          decimalsInFloat: 3,
          min: 0,
          title: {
            text: "Value"
          }
        }
      };
    },
    values() {
      return (
        this.$store.getters["cusip/historical/getPeriods"].map(
          x => x.price_stats.average_value
        ) || []
      );
    },
    chartLabels() {
      return (
        this.$store.getters["cusip/historical/getPeriods"].map(
          x => x.quarter
        ) || []
      );
    },
    chartSeries() {
      return [
        {
          name: "Value",
          type: "line",
          data: this.values
        }
      ];
    }
  },
  props: {
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
  mounted() {
    const cusip = this.$route.params.cusip;
    this.$store.dispatch("cusip/historical/fetchData", { cusip });
  }
};
</script>
<style></style>
