import Vue from "vue";

const state = {
  holdingsTotal: 0,
  filingCount: 0,
  averageHoldingValue: 0
};

const getters = {
  getHoldingsTotal: s => s.holdingsTotal,
  getFilingCount: s => s.filingCount,
  getAverageHoldingValue: s => s.averageHoldingValue
};

const actions = {
  fetchData: ({ commit, getters }) => {
    Vue.prototype.$axios.get("/api/dashboard/").then(resp => {
      commit("setHoldingsTotal", resp.data.holdings_total);
      commit("setFilingCount", resp.data.filing_count);
      commit("setAverageHoldingValue", resp.data.average_holding_value);
    });
  }
};

const mutations = {
  setHoldingsTotal: (state, payload) => {
    state.holdingsTotal = payload;
  },
  setFilingCount: (state, payload) => {
    state.filingCount = payload;
  },
  setAverageHoldingValue: (state, payload) => {
    state.averageHoldingValue = payload;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
