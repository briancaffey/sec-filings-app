import Vue from "vue";

const state = {
  accountStatus: null,
};

const getters = {
  getAccountStatus: s => s.accountStatus,
};

const actions = {
  fetchData: ({ commit, dispatch }, payload) => {
    Vue.prototype.$axios.post("/api/account/", payload).then(resp => {
      commit("setAccount", resp);
    });
  },
};

const mutations = {
  setAccount: (state, payload) => {
    state.accountStatus = payload.account_status;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
