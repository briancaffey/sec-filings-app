import FundScatterplot from "components/charts/FundScatterplot.vue";
import HistoricalHoldingsChart from "components/charts/HistoricalHoldingsChart.vue";
import PortfolioSummary from "components/PortfolioSummary.vue";
import PortfolioHoldingsByPeriodChart from "components/charts/PortfolioHoldingsByPeriodChart.vue";
import HistoricalPortfolioValueChart from "components/charts/HistoricalPortfolioValueChart.vue";
import PortfolioHoldingsByPeriodTable from "components/tables/PortfolioHoldingsByPeriodTable.vue";
import CiksByCusipTable from "components/tables/CiksByCusipTable.vue";
import InvestorsTable from "components/tables/InvestorsTable.vue";
import HoldingsTable from "components/tables/HoldingsTable.vue";
import SecuritiesTable from "components/tables/SecuritiesTable.vue";
import FilingsTable from "components/tables/FilingsTable.vue";
import PeriodSelect from "components/PeriodSelect.vue";

export default async ({ Vue }) => {
  Vue.component("FundScatterplot", FundScatterplot);
  Vue.component("HistoricalHoldingsChart", HistoricalHoldingsChart);
  Vue.component("HoldingsTable", HoldingsTable);
  Vue.component("FilingsTable", FilingsTable);
  Vue.component("HistoricalPortfolioValueChart", HistoricalPortfolioValueChart);
  Vue.component("PeriodSelect", PeriodSelect);
  Vue.component(
    "PortfolioHoldingsByPeriodChart",
    PortfolioHoldingsByPeriodChart
  );
  Vue.component(
    "PortfolioHoldingsByPeriodTable",
    PortfolioHoldingsByPeriodTable
  );
  Vue.component("CiksByCusipTable", CiksByCusipTable);
  Vue.component("PortfolioSummary", PortfolioSummary);
  Vue.component("InvestorsTable", InvestorsTable);
  Vue.component("SecuritiesTable", SecuritiesTable);
};
