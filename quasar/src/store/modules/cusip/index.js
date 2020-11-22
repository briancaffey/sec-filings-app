import Vue from "vue";
import historical from "./historical/index.js";
import holdingCiks from "./holdingCiks/index.js";

const state = {
  companyName: null,
  ciksByCusip: []
};

const getters = {
  getCompanyName: s => s.companyName,
  getCiksByCusip: s => s.ciksByCusip
};

const actions = {
  fetchData: ({ commit, rootGetters }, payload) => {
    const period = rootGetters["core/getPeriod"].value;
    Vue.prototype.$axios.get(`/api/cusip/${payload}/${period}/`).then(resp => {
      commit("setData", resp.data);
    });
  },
  fetchCiksByCusip: ({ commit }, payload) => {
    Vue.prototype.$axios.get(`/api/cusip/${payload}/cik/`).then(resp => {
      commit("setCiksByCusip", resp.data);
    });
  }
};

const mutations = {
  setData: (state, payload) => {
    state.companyName = payload.company_name;
  },
  setCiksByCusip: (state, payload) => {
    console.log(payload);
    state.ciksByCusip = payload;
  }
};

const modules = {
  namespaced: true,
  historical,
  holdingCiks
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
  modules
};
