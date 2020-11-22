import Vue from "vue";

const state = {
  periods: []
};

const getters = {
  getPeriods: s => s.periods
};

const actions = {
  fetchData: ({ commit }, payload) => {
    const { cusip } = payload;
    Vue.prototype.$axios.get(`/api/cusip/${cusip}/historical/`).then(resp => {
      console.log(resp.data);
      commit("setData", resp.data);
    });
  }
};

const mutations = {
  setData: (state, payload) => {
    state.periods = payload;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
