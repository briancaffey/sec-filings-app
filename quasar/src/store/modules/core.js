import Vue from "vue";

export default {
  namespaced: true,
  state: {
    periods: [],
    period: { value: "-", label: "-" }
  },
  getters: {
    getPeriods: s => {
      const options = s.periods.map(x => {
        return { value: x.quarter, label: x.quarter_name };
      });
      return options;
    },
    getPeriod: s => s.period
  },
  mutations: {
    setPeriods(state, payload) {
      state.periods = payload;
    },
    setPeriod(state, payload) {
      state.period = payload;
    }
  },
  actions: {
    setPeriod: ({ commit, dispatch }, payload) => {
      commit("setPeriod", payload);
    },
    getPeriods({ commit, getters }) {
      if (getters.getPeriods === []) return;
      Vue.prototype.$axios.get("/api/filing-periods/").then(resp => {
        commit("setPeriods", resp.data);
        const mostRecentPeriod = resp.data[resp.data.length - 1];
        commit("setPeriod", {
          value: mostRecentPeriod.quarter,
          label: mostRecentPeriod.quarter_name
        });
      });
    }
  }
};
