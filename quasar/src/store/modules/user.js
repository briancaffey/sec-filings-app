import Vue from "vue";

const state = {
  accountStatus: {
    email: null,
    is_staff: null,
    is_superuser: null,
    stripe_customer_id: null,
    subscription: {}
  }
};

const getters = {
  getAccountStatus: s => s.accountStatus
};

const actions = {
  fetchData: ({ commit }, payload) => {
    Vue.prototype.$axios
      .get("/api/account/", payload)
      .then(resp => {
        commit("setAccount", resp);
      })
      .catch(() => {
        // the user is not logged in
        console.log("user is not logged in");
      });
  }
};

const mutations = {
  setAccount: (state, payload) => {
    state.accountStatus = payload.data;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
